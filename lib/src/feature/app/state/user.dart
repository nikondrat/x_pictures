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

  @action
  void getUserData() {
    restClient.get(Endpoint().getAccountInfo).then((value) {
      user = User.fromJson(value!);
    });
  }

  void deleteAccount() {
    restClient.delete(Endpoint().deleteAccount).then((value) {
      user = User.fromJson(value!);

      tokenStorage.clearTokenPair();

      router.goNamed(AppViews.init);
    });
  }

  @action
  void logout() {
    tokenStorage.clearTokenPair();
    setIsLoggedIn(false);

    router.goNamed(AppViews.init);
  }
}
