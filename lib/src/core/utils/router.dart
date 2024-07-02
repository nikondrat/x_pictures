import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:x_pictures/src/data.dart';

abstract class AppViews {
  static const init = 'init';
  static const signIn = 'signIn';
  static const verify = 'verify';

  static const String homePageRoute = 'homePage';
  static const String viewAllPageRoute = 'viewAllPage';
  static const String bottomNavBarControllerPageRoute = 'bottomNavBarPage';
  static const String officePageRoute = 'officePage';
  static const String disclaimarPageRoute = 'disclaimarPage';
  static const String instructionPageRoute = 'instructionPage';
  static const String uploadingPhotosPageRoute = 'uploadingPhotosPage';

  static const String generateView = 'generateView';
  static const String resultView = 'resultView';
}

final GlobalKey<NavigatorState> navKey = GlobalKey();

final GoRouter router = GoRouter(navigatorKey: navKey, routes: [
  // GoRoute(path: '/', builder: (_, __) => GenerationResult())
  GoRoute(
      name: AppViews.init,
      path: _Paths.init,
      builder: (context, state) => const InitView(),
      routes: [
        GoRoute(
            name: AppViews.signIn,
            path: _Paths.signIn,
            builder: (context, state) => const SignInView(),
            routes: [
              GoRoute(
                name: AppViews.verify,
                path: _Paths.verify,
                builder: (context, state) => const VerifyView(),
              ),
            ]),
      ]),
  GoRoute(
      name: AppViews.homePageRoute,
      path: _Paths.homePageRoute,
      builder: (context, state) => const BottomNavBarControllerPage(),
      routes: [
        GoRoute(
            name: AppViews.officePageRoute,
            path: _Paths.officePageRoute,
            builder: (context, state) => const OfficePage(),
            routes: [
              GoRoute(
                  name: AppViews.disclaimarPageRoute,
                  path: _Paths.disclaimarPageRoute,
                  builder: (context, state) => const DisclaimarPage(),
                  routes: [
                    GoRoute(
                        name: AppViews.instructionPageRoute,
                        path: _Paths.instructionPageRoute,
                        builder: (context, state) => const InstructionPage(),
                        routes: [
                          GoRoute(
                            name: AppViews.uploadingPhotosPageRoute,
                            path: _Paths.uploadingPhotosPageRoute,
                            builder: (context, state) =>
                                const UploadingPhotosPage(),
                          )
                        ]),
                  ]),
            ]),
        GoRoute(
            path: _Paths.viewAllPageRoute,
            name: AppViews.viewAllPageRoute,
            builder: (context, state) => const ViewAllPage()),
        GoRoute(
            path: _Paths.generateView,
            name: AppViews.generateView,
            builder: (context, state) => const GenerateView(),
            routes: [
              GoRoute(
                  path: _Paths.resultView,
                  name: AppViews.resultView,
                  builder: (context, state) => const GenerationResult()),
            ]),
      ]),
]);

abstract class _Paths {
  static const init = '/';
  static const signIn = AppViews.signIn;
  static const verify = AppViews.verify;

  static const String homePageRoute = '/${AppViews.homePageRoute}';
  static const String viewAllPageRoute = AppViews.viewAllPageRoute;
  static const String officePageRoute = AppViews.officePageRoute;
  static const String disclaimarPageRoute = AppViews.disclaimarPageRoute;
  static const String instructionPageRoute = AppViews.instructionPageRoute;
  static const String uploadingPhotosPageRoute =
      AppViews.uploadingPhotosPageRoute;

  static const String generateView = AppViews.generateView;
  static const String resultView = AppViews.resultView;
}
