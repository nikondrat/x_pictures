import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:network_info_plus/network_info_plus.dart';
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
                  Gap(30.h),
                  const InputGroup(),
                  const Gap(AppValues.kPadding)
                ],
              );
            },
          )),
    );
  }
}
