
# REC BMS for Home Assistant

This is a Non official [custom integration](https://developers.home-assistant.io/docs/creating_component_index/) for *[Home Assistant](https://www.home-assistant.io/)* via [HACS](https://hacs.xyz/) to surface *[REC BMS](https://www.rec-bms.com/)* (Battery Management System) 


# Supported Entities

This allows you home assistant to connect to REC BMS sensor and display:
- Time remaining (Hours)
- Minimum cell voltage (Voltage)
- Maximum cell voltage" (Voltage)
- Battery current (Amps)
- Max Temperature (C)
- Pack Voltage" (Voltage)
- State of Charge (Percent)
- State of Health (Percent)

# Install

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=tiagonmas&repository=recbms&category=integration)

## Install via HACS

- The installation is done inside [HACS](https://hacs.xyz/) (Home Assistant Community Store). If you don't have HACS, you must install it before adding this integration. [Installation instructions here.](https://hacs.xyz/docs/setup/download)
- Once HACS is installed, search for `recbms`
  - Navigate to the 'Integrations' tab in HACS, click `explore & Download` and search for the 'recbms' integration there. On the next screen, select "Download". Once fully downloaded, restart HomeAssistant.
- In the sidebar, click 'Configuration', then 'Devices & Services'. Click the + icon to add "recbms" to your Home Assistant installation.
  - Enter the host or IP of your RECBMS websocket (the ip or host and it ends with "/ws")
  - Enter the name you want to show for your REC BMS

# Support

You have issue with the integration, you want new sensors? Please open an [Issue](https://github.com/tiagonmas/recbms/issues).

# Screenshot

soon
