import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:go_router/go_router.dart';
import 'package:network_info_plus/network_info_plus.dart';
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
        Provider<SignInViewStore>(
          create: (_) => SignInViewStore(),
          dispose: (context, value) => value.dispose(),
        ),
        Provider<NetworkInfo>(
          create: (_) => NetworkInfo(),
        ),
        Provider(
          create: (context) => AuthStore(
              restClient: context.read<Dependencies>().restClient,
              tokenStorage: context.read<Dependencies>().tokenStorage,
              signInViewStore: context.read(),
              networkInfo: context.read()),
        ),
      ],
      builder: (context, _) => Scaffold(
          appBar: AppBar(
            leading: const CustomBackButton(),
            title: AutoSizeText(
              t.auth.title,
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
                      title: t.auth.hint.add, description: t.auth.description),
                  Gap(30.h),
                  const InputGroup(),
                  const Gap(AppValues.kPadding / 2),
                  GestureDetector(
                    onTap: () => context.pushNamed(AppViews.forgot,
                        extra: {'store': context.read<SignInViewStore>()}),
                    child: Center(
                      child: AutoSizeText(
                        '${t.auth.hint.forgot_password.title}?',
                        maxFontSize: 24,
                        style: textTheme.bodyLarge!.copyWith(
                          fontSize: 14.sp,
                        ),
                      ),
                    ),
                  )
                ],
              );
            },
          )),
    );
  }
}
