import 'dart:convert';
import 'dart:io';

import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'user.g.dart';

class UserStore extends _UserStore with _$UserStore {
  UserStore({required super.restClient, required super.tokenStorage});
}

abstract class _UserStore with Store {
  final RestClient restClient;
  final TokenStorage tokenStorage;

  _UserStore({required this.restClient, required this.tokenStorage});

  @observable
  User user = User(
    id: '',
    username: '',
    email: '',
    imageUrl: '',
    balance: '',
    profileType: ProfileType.basic,
    typeVerbose: '',
    isVerified: false,
    subscription: Subscription(
      id: '',
      title: '',
      isActive: false,
      startDate: DateTime.now(),
      endDate: DateTime.now(),
    ),
    created: DateTime.now(),
    updated: DateTime.now(),
  );

  @observable
  bool isLoggedIn = false;

  @action
  void setIsLoggedIn(bool value) => isLoggedIn = value;

  @computed
  String? get username => user.username;

  @computed
  String get email => user.email;

  @computed
  String? get imageUrl => user.imageUrl;

  @computed
  String get balance => user.balance;

  @observable
  Patreon? patreon;

  /// Function to get user data
  @action
  void getUserData() {
    restClient.get(Endpoint().getAccountInfo).then((value) {
      user = User.fromJson(value!);
    }).catchError((error) {
      // TODO only for development
      user = User(
        id: '1',
        username: 'Ivan Ivanov',
        email: 'nice@ya.ru',
        imageUrl:
            'https://n1s2.hsmedia.ru/fd/0b/da/fd0bdab6296e49f4aabe276afa93f3fb/5146x3425_0xc0a839a2_18538190921484896142.jpeg',
        balance: 'balance',
        profileType: ProfileType.basic,
        typeVerbose: 'Basic',
        isVerified: true,
        subscription: Subscription(
          id: '1',
          title: 'title',
          isActive: true,
          startDate: DateTime.now(),
          endDate: DateTime.now(),
        ),
        created: DateTime.now(),
        updated: DateTime.now(),
      );
    });
  }

  /// Function to change password
  void changePassword(String oldPassword, String newPassword) {
    restClient.post(Endpoint().changePassword, body: {
      "password": oldPassword,
      "new_password": newPassword
    }).then((value) {
      user = User.fromJson(value!);
    });
  }

  /// Function to update username
  @action
  void updateAccount(String username) {
    restClient.post(Endpoint().updateAccount, body: {
      "username": username,
    }).then((value) {
      user = User.fromJson(value!);
    });
  }

  @action
  Future uploadImage(File image) async {
    restClient.post(Endpoint().uploadImage,
        body: {'image': base64Encode(await image.readAsBytes())});
  }

  /// Function to activate patreon
  @action
  void activatePatreon(String code) {
    restClient.post(Endpoint().patreon, body: {"code": code}).then((value) {
      patreon = Patreon.fromJson(value!);
    });
  }

  /// Function to get patreon info
  @action
  void getPatreonInfo() {
    restClient.get(Endpoint().patreonInfo).then((value) {
      patreon = Patreon.fromJson(value!);
    });
  }

  /// Function to delete image
  @action
  void deleteImage() {
    // TODO maybe need add id of image in path
    restClient.delete(Endpoint().deleteImage).then((value) {
      user = User.fromJson(value!);
    });
  }

  /// Function to delete account
  @action
  void deleteAccount() {
    restClient.delete(Endpoint().deleteAccount).then((value) {
      user = User.fromJson(value!);

      tokenStorage.clearTokenPair();

      router.goNamed(AppViews.init);
    });
  }

  /// Function to logout
  @action
  void logout() {
    tokenStorage.clearTokenPair();
    setIsLoggedIn(false);

    router.goNamed(AppViews.init);
  }
}
