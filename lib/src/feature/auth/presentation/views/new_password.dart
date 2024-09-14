import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class NewPasswordView extends StatelessWidget {
  const NewPasswordView({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return Provider(
      create: (context) => NewPasswordStore(
        restClient: context.read<Dependencies>().restClient,
        tokenStorage: context.read<Dependencies>().tokenStorage,
      ),
      dispose: (context, value) => value.dispose(),
      child: Scaffold(
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
        body: AppBody(
          builder: (windowWidth, windowHeight, windowSize) {
            return ListView(
              padding: HorizontalSpacing.centered(windowWidth),
              children: [
                const Gap(AppValues.kPadding),
                TitleWithDesc(
                    title: t.auth.hint.forgot_password.new_password,
                    description: t.auth.hint.forgot_password.new_password_hint),
                const Gap(AppValues.kPadding),
                NewPasswordGroup(),
              ],
            );
          },
        ),
      ),
    );
  }
}
