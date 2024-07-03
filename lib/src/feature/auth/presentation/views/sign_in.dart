import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';
import 'package:x_pictures/src/feature/auth/presentation/widgets/input_group.dart';

class SignInView extends StatelessWidget {
  const SignInView({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        Provider<SignInViewStore>(
          create: (_) => SignInViewStore(),
          dispose: (context, value) => value.dispose(),
        ),
        Provider(
          create: (context) => AuthStore(signInViewStore: context.read()),
        ),
      ],
      child: Scaffold(
          appBar: AppBar(
            leading: const CustomBackButton(),
            title: Text(t.auth.title),
          ),
          body: AppBody(
            builder: (windowWidth, windowHeight, windowSize) {
              return ListView(
                padding: HorizontalSpacing.centered(windowWidth),
                children: [
                  const Gap(AppValues.kPadding),
                  TitleWithDesc(
                      title: t.auth.hint.add, description: t.auth.description),
                  const Gap(AppValues.kPadding * 2),
                  const InputGroup(),
                  const Gap(AppValues.kPadding)
                ],
              );
            },
          )),
    );
  }
}
