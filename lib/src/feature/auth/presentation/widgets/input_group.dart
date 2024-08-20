import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:reactive_forms/reactive_forms.dart';
import 'package:x_pictures/src/data.dart';

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
                  validationMessages: {'notFound': (c) => t.auth.errors.email},
                  style: textTheme.titleLarge!.copyWith(
                      color: colorScheme.onSecondary, fontSize: 12.sp),
                  textInputAction: TextInputAction.next,
                  decoration: InputDecoration(
                    contentPadding: EdgeInsets.symmetric(
                        horizontal: AppValues.kPadding, vertical: 14.h),
                    hintStyle: textTheme.titleLarge!
                        .copyWith(color: colorScheme.outline, fontSize: 17.sp),
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
                  onSubmitted: (_) => authStore.login(),
                  style: textTheme.titleLarge!.copyWith(
                      color: colorScheme.onSecondary, fontSize: 12.sp),
                  textInputAction: TextInputAction.done,
                  decoration: InputDecoration(
                    contentPadding: EdgeInsets.symmetric(
                        horizontal: AppValues.kPadding, vertical: 14.h),
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
                        .copyWith(color: colorScheme.outline, fontSize: 17.sp),
                    hintText:
                        t.auth.hint.input(t: t.auth.password.toLowerCase()),
                  ),
                );
              }),
            ),
            Gap(10.h),
            Observer(
                builder: (_) => GradientButton(
                    onPressed: authStore.login,
                    isEnabled: store.isValid,
                    text: t.common.continue_action))
          ],
        ));
  }
}
