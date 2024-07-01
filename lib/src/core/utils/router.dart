import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:x_pictures/src/data.dart';

abstract class AppViews {
  static const init = 'init';
  static const signIn = 'signIn';
}

final GlobalKey<NavigatorState> navKey = GlobalKey();

final GoRouter router = GoRouter(navigatorKey: navKey, routes: [
  GoRoute(path: '/', builder: (_, __) => SignInView())
  // TODO
  // GoRoute(
  //     name: AppViews.init,
  //     path: _Paths.init,
  //     builder: (context, state) => const InitView(),
  //     routes: [
  //       GoRoute(
  //         name: AppViews.signIn,
  //         path: _Paths.signIn,
  //         builder: (context, state) => const SignInView(),
  //       ),
  //     ])
]);

abstract class _Paths {
  static const init = '/';
  static const signIn = AppViews.signIn;
}
