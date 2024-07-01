import 'package:mobx/mobx.dart';
import 'package:reactive_forms/reactive_forms.dart';

part 'view.g.dart';

class SignInViewStore extends _SignInViewStore with _$SignInViewStore {
  SignInViewStore();
}

abstract class _SignInViewStore with Store {
  @observable
  bool isShowPassword = false;

  @action
  void toggleShowPassword() {
    isShowPassword = !isShowPassword;
  }

  final FormGroup formGroup = FormGroup({
    "email": FormControl(validators: [
      Validators.required,
    ]),
    "password": FormControl<String>(validators: [
      Validators.required,
      Validators.minLength(8),
    ]),
  });

  @computed
  bool get isValid => formGroup.valid;

  void dispose() {
    formGroup.dispose();
  }
}
