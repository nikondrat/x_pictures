import 'package:flutter/foundation.dart';
import 'package:mobx/mobx.dart';
import 'package:reactive_forms/reactive_forms.dart';
import 'package:x_pictures/src/data.dart';

part 'forgot_password.g.dart';

class ForgotPasswordStore extends _ForgotPasswordStore
    with _$ForgotPasswordStore {
  ForgotPasswordStore({
    required super.restClient,
    required super.email,
  });
}

abstract class _ForgotPasswordStore with Store {
  final RestClient restClient;
  final String? email;

  _ForgotPasswordStore({
    required this.restClient,
    required this.email,
  });

  late final FormGroup formGroup = FormGroup({
    'email': FormControl<String>(
      value: email,
      validators: [
        Validators.required,
        Validators.email,
      ],
    )
  });

  void dispose() {
    formGroup.dispose();
  }

  Future reqNewPassword() async {
    final String email = formGroup.control('email').value;

    if (kDebugMode) {
      router.pushNamed(AppViews.verify);
    } else {
      restClient.post(Endpoint().sendReqPasswordReset, body: {
        'email': email,
      }).then((value) {
        router.pushNamed(AppViews.verify);
      });
    }
  }
}
