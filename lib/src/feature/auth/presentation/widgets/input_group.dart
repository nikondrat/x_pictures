import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:reactive_forms/reactive_forms.dart';
import 'package:x_pictures/src/data.dart';

import 'input.dart';

class InputGroup extends StatelessWidget {
  const InputGroup({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;
    final SignInViewStore store = context.watch<SignInViewStore>();
    final AuthStore authStore = context.watch<AuthStore>();

    return ReactiveForm(
        formGroup: store.formGroup,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            InputWithTitleWidget(
              title: t.init.providers.email,
              inputWidget: ReactiveTextField(
                  formControlName: 'email',
                  style: textTheme.titleLarge!
                      .copyWith(color: colorScheme.onSecondary),
                  decoration: InputDecoration(
                    contentPadding: const EdgeInsets.all(AppValues.kPadding),
                    hintStyle: textTheme.titleLarge!
                        .copyWith(color: colorScheme.outline),
                    hintText: t.auth.hint
                        .input(t: t.init.providers.email.toLowerCase()),
                  )),
            ),
            InputWithTitleWidget(
              title: t.auth.password,
              inputWidget: Observer(builder: (_) {
                return ReactiveTextField(
                  formControlName: 'password',
                  obscuringCharacter: '•',
                  obscureText: !store.isShowPassword,
                  style: textTheme.titleLarge!
                      .copyWith(color: colorScheme.onSecondary),
                  decoration: InputDecoration(
                    contentPadding: const EdgeInsets.all(AppValues.kPadding),
                    suffixIcon: Padding(
                      padding: const EdgeInsets.only(right: AppValues.kPadding),
                      child: IconButton(
                        onPressed: store.toggleShowPassword,
                        icon: Icon(
                          store.isShowPassword
                              ? Icons.visibility
                              : Icons.visibility_off,
                          color: colorScheme.primary,
                        ),
                      ),
                    ),
                    hintStyle: textTheme.titleLarge!
                        .copyWith(color: colorScheme.outline),
                    hintText:
                        t.auth.hint.input(t: t.auth.password.toLowerCase()),
                  ),
                );
              }),
            ),
            const Gap(AppValues.kPadding),
            GradientButton(
                onPressed: authStore.signIn, text: t.common.continue_action)
          ],
        ));
  }
}
