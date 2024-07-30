import 'package:mobx/mobx.dart';

part 'home.g.dart';

class HomeStore extends _HomeStore with _$HomeStore {
  HomeStore();
}

abstract class _HomeStore with Store {
  @observable
  bool showBottomBar = true;

  @action
  void setShowBottomBar(bool value) {
    showBottomBar = value;
  }
}
