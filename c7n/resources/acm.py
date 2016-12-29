# Copyright 2016 Capital One Services, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from c7n.manager import resources
from c7n.query import QueryResourceManager
from c7n.utils import local_session


@resources.register('acm-certificate')
class Certificate(QueryResourceManager):

    class resource_type(object):
        service = 'acm'
        enum_spec = ('list_certificates', 'CertificateSummaryList', None)
        id = 'CertificateArn'
        name = 'DomainName'
        date = 'CreatedAt'
        dimension = None
        config_type = "AWS::ACM::Certificate"

    def augment(self, resources):

        def _augment(r):
            client = local_session(self.session_factory).client('acm')
            attrs = client.describe_certificate(
                CertificateArn=r)['Certificate']
            r.update(attrs)
            return r

        with self.executor_factory(max_workers=3) as w:
            return list(w.map(_augment, resources))
