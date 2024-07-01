import 'dart:async';

import 'package:mobx/mobx.dart';
import 'package:reactive_forms/reactive_forms.dart';

part 'view.g.dart';

class SignInViewStore extends _SignInViewStore with _$SignInViewStore {
  SignInViewStore();
}

abstract class _SignInViewStore with Store {
  _SignInViewStore() {
    _valueChangesSubscription = formGroup.valueChanges.listen((_) {
      isValid = formGroup.valid;
    });
  }
  @observable
  bool isShowPassword = false;

  @action
  void toggleShowPassword() {
    isShowPassword = !isShowPassword;
  }

  final FormGroup formGroup = FormGroup({
    "email": FormControl(validators: [
      Validators.required,
      Validators.email,
    ]),
    "password": FormControl<String>(validators: [
      Validators.required,
      Validators.minLength(8),
    ]),
  });

  @observable
  bool isValid = false;

  late StreamSubscription _valueChangesSubscription;

  void dispose() {
    formGroup.dispose();
    _valueChangesSubscription.cancel();
    stopTimer();
  }

  Timer? _timer;

  @observable
  int seconds = 0;

  @action
  void startTimer() {
    _timer?.cancel();
    _timer = Timer.periodic(Duration(seconds: 20), (timer) {
      seconds++;
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
