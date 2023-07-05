from django.shortcuts import render

# Integrations
from domain.taigas.integrations.integration_epics import get_epics_from_project_template
from domain.taigas.integrations.integration_projects import get_all_projects

# Logging
import logging

logger = logging.getLogger(__name__)


def ManagementEpicsView(request):
    context = {}
    epics = get_epics_from_project_template()
    projects = get_all_projects()
    logger.info(epics)
    context['epics'] = epics
    context['projects'] = projects
    return render(request, 'management/epics/index.html', context)
