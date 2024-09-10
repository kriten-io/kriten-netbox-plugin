from netbox.api.routers import NetBoxRouter
from . import views


app_name = 'kriten_netbox'

router = NetBoxRouter()
router.register('kriten-clusters', views.KritenClusterViewSet)
router.register('kriten-runners', views.KritenRunnerViewSet)
router.register('kriten-tasks', views.KritenTaskViewSet)
router.register('kriten-jobs', views.KritenJobViewSet)

urlpatterns = router.urls