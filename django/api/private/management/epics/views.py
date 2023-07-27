from django.shortcuts import render

# Integrations
from domain.taigas.integrations.integration_auth import fetch_root_auth_data
from domain.taigas.integrations.integration_epics import get_epics_from_project_template
from domain.taigas.integrations.integration_projects import get_all_projects

# Logging
import logging

logger = logging.getLogger(__name__)


def ManagementEpicsView(request):

    context = {}

    auth_data = fetch_root_auth_data()
    auth_token = auth_data.auth_token

    epics = get_epics_from_project_template(auth_token=auth_token)
    projects = get_all_projects(auth_token=auth_token)

    logger.info(epics)

    context['epics'] = epics
    context['projects'] = projects

    return render(request, 'management/epics/index.html', context)
