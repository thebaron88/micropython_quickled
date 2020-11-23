#include "driver/rmt.h"
#include "py/mphal.h"

#define K255 255
#define K171 171
#define K85  85

struct CRGB {
    uint8_t g;
    uint8_t r;
    uint8_t b;
};

struct CHSV {
    uint8_t h;
    uint8_t s;
    uint8_t v;
};

typedef uint8_t fract8;

uint8_t scale8( uint8_t i, fract8 scale) {
    return ((int)i * (int)(scale) ) >> 8;
}

uint8_t scale8_video_LEAVING_R1_DIRTY( uint8_t i, fract8 scale) {
    return (((int)i * (int)scale) >> 8) + ((i && scale) ? 1 : 0 );
}

uint8_t scale8_LEAVING_R1_DIRTY( uint8_t i, fract8 scale) {
    return ((int)i * (int)(scale) ) >> 8;
}

void hsv2rgb_rainbow_mark(struct CHSV *hsv, struct CRGB *rgb) {
    uint8_t hue = hsv->h;
    uint8_t sat = hsv->s;
    uint8_t val = hsv->v;

    uint8_t offset = hue & 0x1F; // 0..31

    // offset8 = offset * 8
    uint8_t offset8 = offset * 8;
    uint8_t third = scale8( offset8, (256 / 3));

    uint8_t r, g, b;

    if( hue < 32 ) {
        //case 0: // R -> O
        r = K255 - third;
        g = third;
        b = 0;
    } else if ( hue < 64 ){
        //case 1: // O -> Y
        r = K171;
        g = K85 + third ;
        b = 0;
    } else if ( hue < 96 ){
        //case 2: // Y -> G
        uint8_t twothirds = scale8( offset8, ((256 * 2) / 3));
        r = K171 - twothirds;
        g = K171 + third;
        b = 0;
    } else if ( hue < 128 ){
        // case 3: // G -> A
        r = 0;
        g = K255 - third;
        b = third;
    } else if ( hue < 160 ){
        //case 4: // A -> B
        r = 0;
        uint8_t twothirds = scale8( offset8, ((256 * 2) / 3));
        g = K171 - twothirds;
        b = K85  + twothirds;
    } else if ( hue < 192 ) {
        //case 5: // B -> P
        r = third;
        g = 0;
        b = K255 - third;
    } else if ( hue < 224 ) {
        //case 6: // P -- K
        r = K85 + third;
        g = 0;
        b = K171 - third;
    } else {
        //case 7: // K -> R
        r = K171 + third;
        g = 0;
        b = K85 - third;
    }

    // Scale down colors if we're desaturated at all
    // and add the brightness_floor to r, g, and b.
    if( sat != 255 ) {
        if( sat == 0) {
            r = 255; b = 255; g = 255;
        } else {
            if( r ) r = scale8( r, sat) + 1;
            if( g ) g = scale8( g, sat) + 1;
            if( b ) b = scale8( b, sat) + 1;

            uint8_t desat = 255 - sat;
            desat = scale8( desat, desat);

            uint8_t brightness_floor = desat;
            r += brightness_floor;
            g += brightness_floor;
            b += brightness_floor;
        }
    }

    // Now scale everything down if we're at value < 255.
    if( val != 255 ) {
        val = scale8_video_LEAVING_R1_DIRTY( val, val);
        if( val == 0 ) {
            r=0; g=0; b=0;
        } else {
            if( r ) r = scale8( r, val) + 1;
            if( g ) g = scale8( g, val) + 1;
            if( b ) b = scale8( b, val) + 1;
        }
    }

    rgb->r = r;
    rgb->g = g;
    rgb->b = b;
}


STATIC mp_obj_t quickled_write(mp_obj_t pin, mp_obj_t buf) {
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(buf, &bufinfo, MP_BUFFER_READ);

    if (bufinfo.len == 0) {
        return mp_const_none;
    }

    rmt_config_t config;
    config.rmt_mode = RMT_MODE_TX;
    config.channel = (rmt_channel_t)0;
    config.gpio_num = mp_hal_get_pin_obj(pin);
    config.mem_block_num = 1;
    config.tx_config.loop_en = 0;

    config.tx_config.carrier_en = 0;
    config.tx_config.idle_output_en = 1;
    config.tx_config.idle_level = 0;
    config.tx_config.carrier_duty_percent = 50;
    config.tx_config.carrier_freq_hz = 0;
    config.tx_config.carrier_level = 1;

    config.clk_div = 4;

    check_esp_err(rmt_config(&config));
    check_esp_err(rmt_driver_install(config.channel, 0, 0));

    int num_items = bufinfo.len * 8;
    uint8_t *p = (uint8_t *)bufinfo.buf;
    uint8_t pix = *p++;
    uint8_t mask = 0x80;

    rmt_item32_t *items = malloc(num_items * sizeof(rmt_item32_t *));

    for (int item_index = 0; item_index < num_items; item_index++) {
        if (pix & mask) {
            items[item_index].duration0 = 1000/50;
            items[item_index].level0 = 1;
            items[item_index].duration1 = 250/50;
            items[item_index].level1 = 0;
        } else {
            items[item_index].duration0 = 250/50;
            items[item_index].level0 = 1;
            items[item_index].duration1 = 1000/50;
            items[item_index].level1 = 0;
        }
        if (!(mask >>= 1)) {
            pix = *p++;
            mask = 0x80;
        }
    }

    check_esp_err(rmt_write_items(config.channel, items, num_items, true /* blocking */));

    rmt_driver_uninstall(config.channel);
    free(items);

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(quickled_write_obj, quickled_write);


STATIC mp_obj_t quickled_write_hue(mp_obj_t pin, mp_obj_t buf) {
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(buf, &bufinfo, MP_BUFFER_READ);

    if (bufinfo.len == 0) {
        return mp_const_none;
    }

    rmt_config_t config;
    config.rmt_mode = RMT_MODE_TX;
    config.channel = (rmt_channel_t)0;
    config.gpio_num = mp_hal_get_pin_obj(pin);
    config.mem_block_num = 1;
    config.tx_config.loop_en = 0;

    config.tx_config.carrier_en = 0;
    config.tx_config.idle_output_en = 1;
    config.tx_config.idle_level = 0;
    config.tx_config.carrier_duty_percent = 50;
    config.tx_config.carrier_freq_hz = 0;
    config.tx_config.carrier_level = 1;

    config.clk_div = 4;

    check_esp_err(rmt_config(&config));
    check_esp_err(rmt_driver_install(config.channel, 0, 0));

    int num_items = bufinfo.len * 8 * 3;
    uint8_t *buff_ptr = (uint8_t *)bufinfo.buf;
    uint8_t mask = 0x80;

    struct CRGB out_color;
    struct CHSV in_hue;
    in_hue.h = *buff_ptr++;
    in_hue.s = 255;
    in_hue.v = 128;

    hsv2rgb_rainbow_mark(&in_hue, &out_color);
    uint8_t val = *((uint8_t *)&out_color);

    rmt_item32_t *items = malloc(num_items * sizeof(rmt_item32_t *));

    int color = 0;
    for (int item_index = 0; item_index < num_items; item_index++) {
        if (val & mask) {
            items[item_index].duration0 = 1000/50;
            items[item_index].level0 = 1;
            items[item_index].duration1 = 250/50;
            items[item_index].level1 = 0;
        } else {
            items[item_index].duration0 = 250/50;
            items[item_index].level0 = 1;
            items[item_index].duration1 = 1000/50;
            items[item_index].level1 = 0;
        }
        if (!(mask >>= 1)) {
            if (++color == 3) {
                color = 0;
                in_hue.h = *buff_ptr++;
                hsv2rgb_rainbow_mark(&in_hue, &out_color);
            }
            val = *(((uint8_t *)&out_color)+color);
            mask = 0x80;
        }
    }

    check_esp_err(rmt_write_items(config.channel, items, num_items, true /* blocking */));

    rmt_driver_uninstall(config.channel);
    free(items);

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(quickled_write_hue_obj, quickled_write_hue);

STATIC const mp_rom_map_elem_t quickled_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_quickled) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&quickled_write_obj) },
    { MP_ROM_QSTR(MP_QSTR_write_hue), MP_ROM_PTR(&quickled_write_hue_obj) },
};
STATIC MP_DEFINE_CONST_DICT(quickled_module_globals, quickled_module_globals_table);

const mp_obj_module_t quickled_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&quickled_module_globals,
};
MP_REGISTER_MODULE(MP_QSTR_quickled, quickled_cmodule, MODULE_QUICKLED_ENABLED);
