import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';
import 'package:x_pictures/src/feature/auth/presentation/widgets/input_group.dart';

class SignInView extends StatelessWidget {
  const SignInView({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return MultiProvider(
      providers: [
        Provider(
            create: (_) => SignInViewStore(),
            dispose: (context, value) => value.dispose()),
        ProxyProvider<SignInViewStore, AuthStore>(
          update: (_, store, __) => AuthStore(signInViewStore: store),
        ),
      ],
      child: Scaffold(
          appBar: AppBar(
            title: Text(t.auth.title),
            centerTitle: true,
          ),
          body: AppBody(
            builder: (windowWidth, windowHeight, windowSize) {
              return Padding(
                padding: HorizontalSpacing.centered(windowWidth),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const Gap(AppValues.kPadding),
                    Align(
                      alignment: Alignment.center,
                      child: AutoSizeText(
                        t.auth.hint.add,
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
                            t.auth.description,
                            textAlign: TextAlign.center,
                            style: textTheme.headlineSmall!
                                .copyWith(color: themeData.colorScheme.outline),
                            maxLines: 2,
                          ),
                        )),
                    const Gap(AppValues.kPadding),
                    const InputGroup(),
                    const Gap(AppValues.kPadding)
                  ],
                ),
              );
            },
          )),
    );
  }
}
