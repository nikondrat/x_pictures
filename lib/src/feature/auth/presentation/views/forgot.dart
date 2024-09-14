import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:reactive_forms/reactive_forms.dart';
import 'package:x_pictures/src/data.dart';

class ForgotPasswordView extends StatelessWidget {
  final SignInViewStore? store;
  const ForgotPasswordView({
    super.key,
    required this.store,
  });

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return Provider(
      create: (context) => ForgotPasswordStore(
          restClient: context.read<Dependencies>().restClient,
          email: store?.formGroup.control('email').value),
      dispose: (context, value) => value.dispose(),
      builder: (context, _) {
        final ForgotPasswordStore store = context.watch<ForgotPasswordStore>();

        return Scaffold(
            appBar: AppBar(
              leading: const CustomBackButton(),
              title: AutoSizeText(
                t.auth.hint.forgot_password.title,
                style: textTheme.bodyMedium!.copyWith(
                  fontWeight: FontWeight.w700,
                  fontSize: 17,
                ),
              ),
            ),
            body: ReactiveForm(
                formGroup: store.formGroup,
                child: AppBody(
                  builder: (windowWidth, windowHeight, windowSize) {
                    return ListView(
                      padding: HorizontalSpacing.centered(windowWidth),
                      children: [
                        const Gap(AppValues.kPadding),
                        TitleWithDesc(
                            title: t.auth.hint.add,
                            description:
                                t.auth.hint.forgot_password.description),
                        Gap(30.h),
                        InputWithTitleWidget(
                          title: t.init.providers.email,
                          inputWidget: ReactiveTextField(
                              formControlName: 'email',
                              onChanged: (control) {
                                control.markAsTouched();
                              },
                              onSubmitted: (control) {
                                if (control.valid) {
                                  store.reqNewPassword();
                                }
                              },
                              style: textTheme.titleLarge!.copyWith(
                                  color: colorScheme.onSecondary,
                                  fontSize: 17.sp),
                              textInputAction: TextInputAction.next,
                              decoration: InputDecoration(
                                contentPadding: EdgeInsets.symmetric(
                                    horizontal: AppValues.kPadding,
                                    vertical: 14.h),
                                hintStyle: textTheme.titleLarge!.copyWith(
                                    color: colorScheme.outline,
                                    fontSize: 17.sp),
                                hintText: t.auth.hint.input(
                                    t: t.init.providers.email.toLowerCase()),
                              )),
                        ),
                        Gap(140.h),
                        ReactiveValueListenableBuilder(
                          formControlName: 'email',
                          builder: (context, control, child) {
                            return GradientButton(
                                onPressed: store.reqNewPassword,
                                isEnabled: control.valid,
                                text: t.common.continue_action);
                          },
                        ),
                        const Gap(AppValues.kPadding / 2),
                      ],
                    );
                  },
                )));
      },
    );
  }
}
