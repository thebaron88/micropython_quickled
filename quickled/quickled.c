#include "driver/rmt.h"
#include "py/mphal.h"


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

STATIC const mp_rom_map_elem_t quickled_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_quickled) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&quickled_write_obj) },
};
STATIC MP_DEFINE_CONST_DICT(quickled_module_globals, quickled_module_globals_table);

const mp_obj_module_t quickled_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&quickled_module_globals,
};
MP_REGISTER_MODULE(MP_QSTR_quickled, quickled_cmodule, MODULE_QUICKLED_ENABLED);
