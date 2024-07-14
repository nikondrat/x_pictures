import 'package:mobx/mobx.dart';
import 'package:network_info_plus/network_info_plus.dart';
import 'package:x_pictures/src/data.dart';
part 'auth.g.dart';

class AuthStore extends _AuthStore with _$AuthStore {
  AuthStore({
    required super.restClient,
    required super.tokenStorage,
    required super.signInViewStore,
    required super.networkInfo,
  });
}

abstract class _AuthStore with Store {
  final RestClient restClient;
  final TokenStorage tokenStorage;
  final SignInViewStore signInViewStore;
  final NetworkInfo networkInfo;

  _AuthStore({
    required this.restClient,
    required this.tokenStorage,
    required this.signInViewStore,
    required this.networkInfo,
  });

  void signIn() async {
    final ipAddress = await networkInfo.getWifiIP();

    restClient.post('users/login/', body: {
      'email': signInViewStore.email,
      'password': signInViewStore.password,
      'ip_address': ipAddress
    }).then((value) {
      final String? token = value?['token'] as String?;

      if (token != null) {
        tokenStorage.saveTokenPair(Future.value(token));
        router.goNamed(AppViews.verify);
      }
    });
  }
}
