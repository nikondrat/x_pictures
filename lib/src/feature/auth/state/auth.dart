import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';
part 'auth.g.dart';

class AuthStore extends _AuthStore with _$AuthStore {
  AuthStore({required super.signInViewStore});
}

abstract class _AuthStore with Store {
  final SignInViewStore signInViewStore;
  _AuthStore({required this.signInViewStore});

  void signIn() {
    // TODO add api func
    router.goNamed(AppViews.verify);
  }
}
