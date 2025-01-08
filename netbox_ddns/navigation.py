from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu

menu = PluginMenu(
    label='DDNS',
    groups=(
        ('Configuration', (
            PluginMenuItem(
                link='plugins:netbox_ddns:server_list',
                link_text='DDNS Servers',
                buttons=[
                    PluginMenuButton(
                        link='plugins:netbox_ddns:server_add',
                        title='Add',
                        icon_class='mdi mdi-plus-thick',
                    )
                ]
            ),
            PluginMenuItem(
                link='plugins:netbox_ddns:zone_list',
                link_text='Forward Zones',
                buttons=[
                    PluginMenuButton(
                        link='plugins:netbox_ddns:zone_add',
                        title='Add',
                        icon_class='mdi mdi-plus-thick',
                    )
                ]
            ),
        ),
      ),
    ),
    icon_class='mdi mdi-router'
)
