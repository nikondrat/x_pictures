import 'dart:developer';

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

  /// Function to sign in
  void login() async {
    final ipAddress = await networkInfo.getWifiIP();

    restClient.post(Endpoint().login, body: {
      'email': signInViewStore.email,
      'password': signInViewStore.password,
      'ip_address': ipAddress
    }).then((value) {
      final String? token = value?['token'] as String?;

      if (token != null) {
        tokenStorage.saveTokenPair(token);
        router.goNamed(AppViews.homePageRoute);
      } else {
        signUp();
      }
    });
  }

  /// Function to sign up
  void signUp() async {
    final ipAddress = await networkInfo.getWifiIP();
    restClient.post(Endpoint().register, body: {
      'email': signInViewStore.email,
      'password': signInViewStore.password,
      'ip_address': ipAddress
    }).then((value) {
      final String? token = value?['token'] as String?;

      if (token != null) {
        tokenStorage.saveTokenPair(token);
        router.goNamed(AppViews.verify);
      } else {
        signInViewStore.formGroup
            .control('email')
            .setErrors({'notFound': true});
        signInViewStore.formGroup.markAllAsTouched();
      }
    });
  }

  /// Function to login with google
  void loginWithGoogle(String code) async {
    final ipAddress = await networkInfo.getWifiIP();

    restClient.post(Endpoint().googleAuth, body: {
      'ip_address': ipAddress,
      'code': code,
    }).then((v) {
      final String? token = v?['token'] as String?;

      if (token != null) {
        tokenStorage.saveTokenPair(token);
        router.goNamed(AppViews.verify);
      }
    });
  }

  /// Function send request for set new password in future
  void sendPasswordReset() {
    restClient.post(Endpoint().sendReqPasswordReset,
        body: {'email': signInViewStore.email}).then((value) {
      // router.goNamed(AppViews.resetPassword);
    });
  }

  /// Function to verification by token
  void verificationByToken(String token) async {
    restClient.get('${Endpoint().verificationByToken}/$token', queryParams: {
      'token': token,
    });
  }

  /// Function to set new password
  void setNewPassword() async {
    final String token = await tokenStorage.loadTokenPair();

    restClient.post(Endpoint().setNewPassword, body: {
      'token': token,
      // TODO change variable if need
      'new_password': signInViewStore.password,
    });
  }

  /// Function to refresh verification
  void refreshVerification() {
    restClient.post(Endpoint().refreshVerification, body: {});
    // router.goNamed(AppViews.verify);
  }
}
