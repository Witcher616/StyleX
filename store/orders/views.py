from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import stripe

from http import HTTPStatus
from django.views.generic import CreateView
from orders.forms import OrderForm
from django.views.generic import TemplateView

from django.urls import reverse, reverse_lazy
from products.models import Basket
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'

class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'

# Create your views here.
class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    title = 'Store - Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    
    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '',
                    'quantity': 1,
                },
            ],
            metadata={'order_id': self.object},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)
    
    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs) -> dict[str]:
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        context['baskets'] = baskets
        context['total_sum'] = sum([(basket.product.price * basket.quantity) for basket in baskets])
        context['total_quantity'] = sum(basket.quantity for basket in baskets)
        return context

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.complited':
        session = event['data']['object']
        
        fulfill_order(session)
    return HttpResponse(status=200)
        
    
def fulfill_order(session):
    #TODO: fill me in
    print('Fullfilling order')
