import 'dart:async';

import 'package:mobx/mobx.dart';

part 'verify.g.dart';

class VerifyStore extends _VerifyStore with _$VerifyStore {}

abstract class _VerifyStore with Store {
  Timer? _timer;

  @observable
  int seconds = 20;

  @action
  void startTimer() {
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (seconds <= 1) {
        stopTimer();
      }
      seconds--;
    });
  }

  @action
  void stopTimer() {
    _timer?.cancel();
  }

  @action
  void resetTimer() {
    _timer?.cancel();
    seconds = 0;
  }
}
