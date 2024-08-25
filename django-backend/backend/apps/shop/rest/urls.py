from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.shop.rest import views
from apps.shop.rest import webhooks
from apps.shop.rest import callbacks

router = SimpleRouter()
router.register('', viewset=views.ProductAPIViewSet, basename='products_set')
router.register('payment', viewset=views.PaymentAPIViewSet, basename='payment_set')

urlpatterns = [
    path('', include(router.urls)),
    path('subscription/cancel/', views.cancel_subscription, name='cancel_subscription'),

    # Webhooks
    path('webhook/ivendpay/', webhooks.ivendpay_webhook, name='ivendpay_webhook'),
    path('webhook/payadmit/', webhooks.payadmit_webhook, name='payadmit_webhook'),
    path('webhook/ark-pay/', webhooks.ark_pay_webhook, name='arkpay_webhook'),

    # Callbacks
    path('callback/paypal/', callbacks.paypal_callback, name='paypal_callback'),
    path('callback/paypal-subscription/', callbacks.paypal_subscription_callback, name='paypal_subscription_callback'),
    path('callback/stripe/', callbacks.stripe_callback, name='stripe_callback'),
    path('callback/emovegan/', callbacks.emovegan_callback, name='emovegan_callback'),

    # For shop
    path('order/', views.create_order_for_shop, name='create_order_for_shop'),
]
