import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'support.g.dart';

class SupportStore extends _SupportStore with _$SupportStore {
  SupportStore({
    required super.restClient,
    required super.userStore,
  });
}

abstract class _SupportStore with Store {
  final RestClient restClient;
  final UserStore userStore;

  _SupportStore({required this.restClient, required this.userStore});

  void sendMessage() {
    restClient.post(Endpoint().sendSupportMessage, body: {
      "name": userStore.user.username,
      "email": userStore.user.email,
      // TODO add text controller value
      "message": 'something'
    });
  }
}
