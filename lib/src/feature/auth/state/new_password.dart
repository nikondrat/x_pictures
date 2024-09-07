import 'package:mobx/mobx.dart';
import 'package:reactive_forms/reactive_forms.dart';
import 'package:x_pictures/src/data.dart';

part 'new_password.g.dart';

class NewPasswordStore extends _NewPasswordStore with _$NewPasswordStore {
  NewPasswordStore({
    required super.restClient,
    required super.tokenStorage,
  });
}

abstract class _NewPasswordStore with Store {
  final RestClient restClient;
  final TokenStorage tokenStorage;

  _NewPasswordStore({
    required this.restClient,
    required this.tokenStorage,
  });

  @observable
  bool isShowPassword = false;

  @action
  void toggleShowPassword() {
    isShowPassword = !isShowPassword;
  }

  @observable
  bool isShowRepeatedPassword = false;

  @action
  void toggleShowRepeatedPassword() {
    isShowRepeatedPassword = !isShowRepeatedPassword;
  }

  final FormGroup formGroup = FormGroup({
    'password': FormControl<String>(validators: [
      Validators.required,
      Validators.minLength(8),
    ]),
    'passwordConfirmation': FormControl<String>(),
  }, validators: [
    const MustMatchValidator(
      'password',
      'passwordConfirmation',
      true,
    )
  ]);

  void dispose() {
    formGroup.dispose();
  }

  Future setNewPassword() async {
    final password = formGroup.control('password').value;
    final token = await tokenStorage.loadTokenPair();

    await restClient.post(Endpoint().setNewPassword,
        body: {"token": token, "new_password": password}).then((v) {
      router.pushReplacementNamed(AppViews.signIn);
    });
  }
}
