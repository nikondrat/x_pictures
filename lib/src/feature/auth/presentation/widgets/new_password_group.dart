import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:reactive_forms/reactive_forms.dart';
import 'package:x_pictures/src/data.dart';

class NewPasswordGroup extends StatelessWidget {
  const NewPasswordGroup({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    final NewPasswordStore store = context.watch<NewPasswordStore>();

    return ReactiveForm(
        formGroup: store.formGroup,
        child:
            Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          InputWithTitleWidget(
            title: t.auth.hint.forgot_password.new_password,
            inputWidget: Observer(builder: (_) {
              return ReactiveTextField(
                  formControlName: 'password',
                  obscuringCharacter: '•',
                  obscureText: !store.isShowPassword,
                  onChanged: (control) {
                    control.markAsTouched();
                  },
                  style: textTheme.titleLarge!.copyWith(
                      color: colorScheme.onSecondary, fontSize: 17.sp),
                  textInputAction: TextInputAction.next,
                  decoration: InputDecoration(
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
                    contentPadding: EdgeInsets.symmetric(
                        horizontal: AppValues.kPadding, vertical: 14.h),
                    hintStyle: textTheme.titleLarge!
                        .copyWith(color: colorScheme.outline, fontSize: 17.sp),
                    hintText: t.auth.hint
                        .input(t: t.init.providers.email.toLowerCase()),
                  ));
            }),
          ),
          InputWithTitleWidget(
            title: t.auth.hint.forgot_password.confirm_password,
            inputWidget: Observer(builder: (_) {
              return ReactiveTextField(
                formControlName: 'passwordConfirmation',
                obscuringCharacter: '•',
                obscureText: !store.isShowRepeatedPassword,
                onSubmitted: (_) => store.setNewPassword(),
                style: textTheme.titleLarge!
                    .copyWith(color: colorScheme.onSecondary, fontSize: 17.sp),
                textInputAction: TextInputAction.done,
                decoration: InputDecoration(
                  contentPadding: EdgeInsets.symmetric(
                      horizontal: AppValues.kPadding, vertical: 14.h),
                  suffixIcon: Padding(
                    padding: const EdgeInsets.only(right: AppValues.kPadding),
                    child: IconButton(
                      onPressed: store.toggleShowRepeatedPassword,
                      icon: Icon(
                        store.isShowRepeatedPassword
                            ? Icons.visibility
                            : Icons.visibility_off,
                        color: colorScheme.primary,
                      ),
                    ),
                  ),
                  hintStyle: textTheme.titleLarge!
                      .copyWith(color: colorScheme.outline, fontSize: 17.sp),
                  hintText: t.auth.hint.input(t: t.auth.password.toLowerCase()),
                ),
              );
            }),
          ),
          Gap(10.h),
          ReactiveValueListenableBuilder(
              formControlName: 'passwordConfirmation',
              builder: (context, passwordControl, child) {
                return GradientButton(
                    onPressed: store.setNewPassword,
                    isEnabled: passwordControl.valid,
                    text: t.common.continue_action);
              })
        ]));
  }
}
