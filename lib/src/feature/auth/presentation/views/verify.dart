import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class VerifyView extends StatelessWidget {
  const VerifyView({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return Provider<VerifyStore>(
      create: (_) => VerifyStore(),
      builder: (context, _) {
        final VerifyStore store = context.watch<VerifyStore>();
        store.startTimer();

        return Scaffold(
          appBar: AppBar(
            leading: const CustomBackButton(),
            title: AutoSizeText(
              t.auth.title,
              style: textTheme.bodyMedium!.copyWith(
                fontWeight: FontWeight.w700,
                fontSize: 17,
              ),
            ),
            centerTitle: true,
          ),
          body: AppBody(
            builder: (windowWidth, windowHeight, windowSize) => ListView(
              padding: HorizontalSpacing.centered(windowWidth),
              children: [
                const Gap(AppValues.kPadding),
                TitleWithDesc(
                    title: t.auth.hint.verify.title,
                    description: t.auth.hint.verify.description),
                const Gap(AppValues.kPadding * 4),
                CustomPinput(
                  windowHeight: windowHeight,
                  windowWidth: windowWidth,
                ),
                // const Gap(AppValues.kPadding * 1.5),
                // GradientButton(
                //     onPressed: () {
                //       router.goNamed(AppViews.homePageRoute);
                //     },
                //     text: t.common.continue_action),
              ],
            ),
          ),
          bottomNavigationBar: Padding(
            padding: EdgeInsets.only(
                bottom: MediaQuery.of(context).viewInsets.bottom +
                    AppValues.kPadding * 2),
            child: Observer(builder: (_) {
              return Text.rich(
                t.auth.hint.verify.did_not_get(
                  value: (c) => TextSpan(
                      style: textTheme.bodyLarge!.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                      recognizer: TapGestureRecognizer()
                        ..onTap = () {
                          // TODO add func
                          // print('tap');
                        },
                      text: '${store.seconds <= 1 ? c : store.seconds}'),
                ),
                textAlign: TextAlign.center,
                style:
                    textTheme.bodyLarge!.copyWith(color: colorScheme.onSurface),
              );
            }),
          ),
        );
      },
    );
  }
}
