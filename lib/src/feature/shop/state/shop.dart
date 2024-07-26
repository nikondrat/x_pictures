import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'shop.g.dart';

class ShopStore extends _ShopStore with _$ShopStore {
  ShopStore({required super.restClient});
}

abstract class _ShopStore with Store {
  final RestClient restClient;

  _ShopStore({required this.restClient});

  @observable
  ObservableFuture<List<Product>> fetchSubscriptionsFuture = emptyResponse;

  @observable
  ObservableList<Product> subscriptions = ObservableList<Product>();

  @observable
  ObservableFuture<List<Product>> fetchProductsFuture = emptyResponse;

  @observable
  ObservableList<Product> products = ObservableList<Product>();

  @observable
  ObservableFuture<List<Gate>> fetchGatesFuture = emptyGatesResponse;

  @observable
  ObservableList<Gate> gates = ObservableList<Gate>();

  @observable
  ObservableFuture<List<Order>> fetchOrdersFuture = emptyOrdersResponse;

  @observable
  ObservableList<Order> orders = ObservableList<Order>();

  @action
  Future getProducts() async {
    final future = restClient.get(Endpoint().shopTokens).then((value) {
      final List<Product> products = value?.values
              .map((e) => Product.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [];
      return products;
    });

    fetchProductsFuture = ObservableFuture(future);

    return products = ObservableList.of(await future);
  }

  @action
  Future getSubscriptions() async {
    final future = restClient.get(Endpoint().getAllSubscriptions).then((value) {
      final List<Product> subscriptions = value?.values
              .map((e) => Product.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [];
      return subscriptions;
    });

    fetchSubscriptionsFuture = ObservableFuture(future);

    return subscriptions = ObservableList.of(await future);
  }

  @action
  Future getGates() async {
    final future = restClient.get(Endpoint().paymentGates).then((value) {
      final GatesBody gates = GatesBody.fromJson(value!);
      return gates.gates;
    });

    fetchGatesFuture = ObservableFuture(future);

    return gates = ObservableList.of(await future);
  }

  @action
  Future getOrders() async {
    final future = restClient.get(Endpoint().paymentOrders).then((value) {
      final OrdersBody orders = OrdersBody.fromJson(value!);
      return orders.orders;
    });

    fetchOrdersFuture = ObservableFuture(future);

    return orders = ObservableList.of(await future);
  }

  @computed
  bool get hasSubscriptionResults =>
      fetchSubscriptionsFuture != emptyResponse &&
      fetchSubscriptionsFuture.status == FutureStatus.fulfilled;

  @computed
  bool get hasProductResults =>
      fetchProductsFuture != emptyResponse &&
      fetchProductsFuture.status == FutureStatus.fulfilled;

  @computed
  bool get hasGatesResults =>
      fetchGatesFuture != emptyGatesResponse &&
      fetchGatesFuture.status == FutureStatus.fulfilled;

  @computed
  bool get hasOrdersResults =>
      fetchOrdersFuture != emptyOrdersResponse &&
      fetchOrdersFuture.status == FutureStatus.fulfilled;

  static ObservableFuture<List<Product>> emptyResponse =
      ObservableFuture.value([]);

  static ObservableFuture<List<Gate>> emptyGatesResponse =
      ObservableFuture.value([]);

  static ObservableFuture<List<Order>> emptyOrdersResponse =
      ObservableFuture.value([]);

  void cancelSubscription() {
    restClient.post(Endpoint().cancelSubscription, body: {});
  }

  void createOrder(String gatewayId) {
    restClient.post(Endpoint().createOrder, body: {
      "gateway_id": gatewayId,
      "currency": "usd",
      "product_id": 0,
      // "extra_data": {

      // }
    }).then((v) {
      final Order data = Order.fromJson(v!);
    });
  }

  @action
  Future<Order?> getPayment(String id) async {
    final Order? order =
        await restClient.get('${Endpoint().paymentOrders}/$id').then((v) {
      final Order data = Order.fromJson(v!);
      return data;
    });
    return order;
  }

  void createPaymentOrder(String gatewayId) {
    restClient.post(Endpoint().createPaymentOrder, body: {
      "currency": "usd",
      "product_id": 0,
      "gateway_id": gatewayId,
      // "extra_data": {}
    });
  }

  void emoveganCallback() {
    restClient.post(Endpoint().emoveganCallback, body: {}).then((v) {
      // final String? action = v?['action'];
      // final String? orderId = v?['order_id'];
    });
  }

  void paypalCallback() {
    restClient.post(Endpoint().paypalCallback, body: {}).then((v) {
      // final String? invoiceId = v?['invoice_id'];
      // final String? subscriptionId = v?['subscription_id'];
    });
  }
}
