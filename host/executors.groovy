// NOTE: Only necessary if using Jenkins workers/nodes/agents

import jenkins.model.*
Jenkins.instance.setNumExecutors(0)
