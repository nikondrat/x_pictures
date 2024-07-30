import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/data.dart';

import '../widgets/button.dart';

class InitView extends StatelessWidget {
  const InitView({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final ColorScheme colorScheme = themeData.colorScheme;

    final TokenStorage tokenStorage = context.read<Dependencies>().tokenStorage;

    // TODO
    tokenStorage.loadTokenPair().then((value) {
      if (value != null) {
        router.goNamed(AppViews.homePageRoute);
      }
    });

    return Scaffold(body: SafeArea(
      child: AppBody(
        builder: (windowWidth, windowHeight, windowSize) {
          return ListView(
            padding: HorizontalSpacing.centered(windowWidth),
            children: [
              const Gap(AppValues.kPadding),
              Image.asset(
                Assets.images.banner.path,
                fit: BoxFit.contain,
                height: windowHeight * .5,
              ),
              const Gap(AppValues.kPadding),
              TitleWithDesc(
                  title: t.init.title, description: t.init.description),
              const Gap(AppValues.kPadding * 2),
              AuthButton(
                windowHeight: windowHeight,
                icon: SvgPicture.asset(Assets.icons.apple),
                title: t.init.sign_in_with(provider: t.init.providers.apple),
                onPressed: () {},
              ),
              const Gap(AppValues.kPadding),
              AuthButton(
                windowHeight: windowHeight,
                icon: SvgPicture.asset(Assets.icons.google),
                title: t.init.sign_in_with(provider: t.init.providers.google),
                onPressed: () {},
              ),
              const Gap(AppValues.kPadding),
              AuthButton(
                windowHeight: windowHeight,
                icon: Icon(
                  Icons.email,
                  color: colorScheme.onSecondary,
                ),
                title: t.init.sign_in_with(provider: t.init.providers.email),
                onPressed: () => router.goNamed(AppViews.signIn),
              ),
              const Gap(AppValues.kPadding)
            ],
          );
        },
      ),
    ));
  }
}
