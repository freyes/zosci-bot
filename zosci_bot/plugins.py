import logging
import re

import click
import openstack
import yaml

from collections import Counter

from mmpy_bot import Plugin, listen_to
from mmpy_bot import Message
from prometheus_api_client import PrometheusConnect


LOG = logging.getLogger(__name__)


class ZOSCIBotPlugin(Plugin):

    def __init__(self, config):
        self._config = config
        #self._cloud = openstack.connect(options=config)
        super().__init__()


class PrometheusPlugin(Plugin):

    SCHEDULED_INSTANCES = 'sum(hypervisor_running_vms{cloud=~"serverstack"})'
    INSTANCES_BY_STATE = ('sum by(instance_state)'
                          '(nova_instances{cloud="serverstack"})')

    def __init__(self, config):
        self._prom = PrometheusConnect(
            url=config['prometheus']['url'],
            disable_ssl=not config['prometheus']['ssl_verify']
        )
        self._config = config
        super().__init__()

    @listen_to("scheduled vms", re.IGNORECASE, needs_mention=True)
    async def scheduled_vms(
            self,
            message: Message,
    ):
        LOG.debug('instances!')
        try:
            data = self._prom.custom_query(self.SCHEDULED_INSTANCES)
            num_instances = data[0]['value'][1]
            data = self._prom.custom_query(self.INSTANCES_BY_STATE)
            msg = f'Scheduled VMs (Total): {num_instances}'
            by_state = {}
            for item in data:
                by_state[item['metric']['instance_state']] = int(item['value'][1])

            msg += '\n {}'.format(yaml.safe_dump(by_state))
            self.driver.reply_to(message, msg)
        except Exception as ex:
            LOG.debug(ex)
            self.driver.reply_to(message,
                                 'Failed to fetch the data from prometheus')
