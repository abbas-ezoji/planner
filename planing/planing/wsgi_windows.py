activate_this = 'C:/Users/ezoji/Envs/planner_venv/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/Users/ezoji/Envs/planner_venv/Lib/site-packages')




# Add the app's directory to the PYTHONPATH
sys.path.append('E:/Projects/planner-master/planner/planing')
sys.path.append('E:/Projects/planner-master/planner/planing/planing')

os.environ['DJANGO_SETTINGS_MODULE'] = 'planing.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planing.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()