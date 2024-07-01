import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/data.dart';

import '../widgets/button.dart';

class InitView extends StatelessWidget {
  const InitView({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);

    final TextTheme textTheme = themeData.textTheme;

    return Scaffold(body: SafeArea(
      child: AppBody(
        builder: (windowWidth, windowHeight, windowSize) {
          return Padding(
            padding: HorizontalSpacing.centered(windowWidth),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Gap(AppValues.kPadding),
                Expanded(
                  child: Image.asset(
                    Assets.images.banner.path,
                    fit: BoxFit.contain,
                  ),
                ),
                const Gap(AppValues.kPadding),
                Align(
                  alignment: Alignment.center,
                  child: AutoSizeText(
                    t.init.title,
                    minFontSize: 16,
                    style: textTheme.displayMedium!
                        .copyWith(fontWeight: FontWeight.bold),
                    maxLines: 1,
                  ),
                ),
                const Gap(AppValues.kPadding),
                Align(
                    alignment: Alignment.center,
                    child: Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: AppValues.kPadding * 2),
                      child: AutoSizeText(
                        t.init.description,
                        textAlign: TextAlign.center,
                        style: textTheme.headlineSmall!
                            .copyWith(color: themeData.colorScheme.outline),
                        maxLines: 2,
                      ),
                    )),
                const Gap(AppValues.kPadding),
                AuthButton(
                  icon: SvgPicture.asset(Assets.icons.apple),
                  title: t.init.sign_in_with(provider: t.init.providers.apple),
                  onPressed: () {},
                ),
                const Gap(AppValues.kPadding),
                AuthButton(
                  icon: SvgPicture.asset(Assets.icons.google),
                  title: t.init.sign_in_with(provider: t.init.providers.google),
                  onPressed: () {},
                ),
                const Gap(AppValues.kPadding),
                AuthButton(
                  icon: Icon(
                    Icons.email,
                    color: themeData.colorScheme.onSecondary,
                  ),
                  title: t.init.sign_in_with(provider: t.init.providers.email),
                  onPressed: () {
                    // TODO add transition
                  },
                ),
                const Gap(AppValues.kPadding)
              ],
            ),
          );
        },
      ),
    ));
  }
}
