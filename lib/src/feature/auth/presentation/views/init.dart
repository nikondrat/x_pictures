import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
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
    // tokenStorage.loadTokenPair().then((value) {
    //   if (value != null) {
    //     router.goNamed(AppViews.homePageRoute);
    //   }
    // });

    return Scaffold(
        body: Container(
      decoration: BoxDecoration(
        image: DecorationImage(
            image: Image.asset(Assets.images.banners.path).image,
            fit: BoxFit.cover),
      ),
      child: SafeArea(
        child: AppBody(
          builder: (windowWidth, windowHeight, windowSize) {
            return Padding(
              padding: HorizontalSpacing.centered(windowWidth),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.end,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Gap(14.h),
                  TitleWithDesc(
                      title: t.init.title, description: t.init.description),
                  Gap(14.h),
                  AutoSizeText('ApiURL: ${Config().apiUrl}'),
                  Gap(14.h),
                  AuthButton(
                    windowHeight: windowHeight,
                    icon: SvgPicture.asset(Assets.icons.apple),
                    title:
                        t.init.sign_in_with(provider: t.init.providers.apple),
                    onPressed: () {},
                  ),
                  Gap(8.h),
                  AuthButton(
                    windowHeight: windowHeight,
                    icon: SvgPicture.asset(Assets.icons.google),
                    title:
                        t.init.sign_in_with(provider: t.init.providers.google),
                    onPressed: () {},
                  ),
                  Gap(8.h),
                  AuthButton(
                    windowHeight: windowHeight,
                    icon: Icon(
                      Icons.email,
                      color: colorScheme.onSecondary,
                    ),
                    title:
                        t.init.sign_in_with(provider: t.init.providers.email),
                    onPressed: () => router.goNamed(AppViews.signIn),
                  ),
                  const Gap(AppValues.kPadding)
                ],
              ),
            );
          },
        ),
      ),
    ));
  }
}
