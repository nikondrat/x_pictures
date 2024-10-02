import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:x_pictures/src/data.dart';

abstract class AppViews {
  static const init = 'init';
  static const signIn = 'signIn';
  static const verify = 'verify';
  static const forgot = 'forgot';
  static const newPassword = 'newPassword';

  static const String homePageRoute = 'homePage';
  static const String viewAllPageRoute = 'viewAllPage';
  static const String bottomNavBarControllerPageRoute = 'bottomNavBarPage';
  static const String officePageRoute = 'officePage';
  static const String disclaimarPageRoute = 'disclaimarPage';
  static const String instructionPageRoute = 'instructionPage';
  static const String uploadingPhotosPageRoute = 'uploadingPhotosPage';

  static const String generateView = 'generateView';
  static const String resultView = 'resultView';
  static const String settingsView = 'settingsView';
  static const String legalView = 'legalView';
  static const String documentView = 'documentView';
  static const String faqView = 'faqView';

  static const String image = 'image';

  static const String allStyles = 'allStyles';
  static const String imageWithBackground = 'imageWithBackground';
  static const String genderView = 'genderView';
  static const String planView = 'planView';
  static const String masterpieceView = 'masterpieceView';

  static const String toolsView = 'toolsView';

  static const String backgroundsView = 'backgroundsView';
  static const String enhanceView = 'enhanceView';
  static const String studyingView = 'studyingView';
  static const String photosView = 'photosView';
}

final GlobalKey<NavigatorState> navKey = GlobalKey();

// final GoRouter router = GoRouter(navigatorKey: navKey, routes: [
//   GoRoute(
//     path: '/',
//     builder: (context, state) =>
//         ProfileView(goHome: () {}, goGenerate: () {}, selectedIndex: 0),
//   )
// ]);

final GoRouter router = GoRouter(navigatorKey: navKey, routes: [
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
                  name: AppViews.forgot,
                  path: _Paths.forgot,
                  builder: (context, state) {
                    final Map? map = state.extra as Map?;
                    final SignInViewStore? store =
                        map?['store'] as SignInViewStore?;
                    return ForgotPasswordView(store: store);
                  },
                  routes: [
                    GoRoute(
                        name: AppViews.verify,
                        path: _Paths.verify,
                        builder: (context, state) => const VerifyView(),
                        routes: [
                          GoRoute(
                            name: AppViews.newPassword,
                            path: _Paths.newPassword,
                            builder: (context, state) =>
                                const NewPasswordView(),
                          ),
                        ]),
                  ]),
            ]),
      ]),
  GoRoute(
      name: AppViews.homePageRoute,
      path: _Paths.homePageRoute,
      builder: (context, state) => const BottomNavBarControllerPage(),
      routes: [
        GoRoute(
            path: _Paths.settingsView,
            name: AppViews.settingsView,
            builder: (context, state) => const SettingsView(),
            routes: [
              GoRoute(
                path: _Paths.faqView,
                name: AppViews.faqView,
                builder: (context, state) => const FaqView(),
              ),
              GoRoute(
                  path: _Paths.legalView,
                  name: AppViews.legalView,
                  builder: (context, state) => const LegalView(),
                  routes: [
                    GoRoute(
                        path: _Paths.documentView,
                        name: AppViews.documentView,
                        builder: (context, state) => DocumentView(
                              title: (state.extra as Map)['title'] ?? '',
                              filePath: (state.extra as Map)['filePath'] ?? '',
                            )),
                  ]),
            ]),
        GoRoute(
            path: _Paths.allStyles,
            name: AppViews.allStyles,
            builder: (context, state) {
              final Map? data = state.extra as Map?;
              final String title = data?['title'] ?? '';
              final onTap = data?['onTap'];
              final items = data?['items'];
              return AllView(
                title: title,
                onTap: onTap,
                packs: items,
              );
            }),
        GoRoute(
            path: _Paths.resultView,
            name: AppViews.resultView,
            builder: (context, state) {
              final Map? data = state.extra as Map?;
              final MediaModel? model = data?['model'];
              final GenerateResponse? response = data?['response'];

              return GenerationResult(
                model: model,
                response: response,
              );
            }),
        GoRoute(
            name: AppViews.officePageRoute,
            path: _Paths.officePageRoute,
            builder: (context, state) {
              final Map? data = state.extra as Map?;
              final PacksStore? store = data?['store'] as PacksStore?;
              return StyleView(
                store: store,
              );
            },
            routes: [
              GoRoute(
                name: AppViews.enhanceView,
                path: _Paths.enhanceView,
                builder: (context, state) {
                  return const EnhanceView();
                },
              ),
              GoRoute(
                  name: AppViews.toolsView,
                  path: _Paths.toolsView,
                  builder: (context, state) {
                    final Map? data = state.extra as Map?;
                    final bool isRemoveBackground =
                        data?['isRemoveBackground'] ?? false;
                    return ToolsView(
                      isRemoveBackground: isRemoveBackground,
                    );
                  },
                  routes: [
                    GoRoute(
                        name: AppViews.backgroundsView,
                        path: _Paths.backgroundsView,
                        builder: (context, state) => const BackgroundsView(),
                        routes: [
                          GoRoute(
                              name: AppViews.imageWithBackground,
                              path: _Paths.imageWithBackground,
                              builder: (_, state) =>
                                  const ImageWithBackgroundResultView())
                        ])
                  ]),
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
                              routes: [
                                GoRoute(
                                    name: AppViews.genderView,
                                    path: _Paths.genderView,
                                    builder: (context, state) {
                                      return const GenderView();
                                    },
                                    routes: [
                                      GoRoute(
                                          name: AppViews.planView,
                                          path: _Paths.planView,
                                          builder: (context, state) {
                                            final Map? data =
                                                state.extra as Map?;
                                            final Function()? continueAction =
                                                data?['continueAction'];
                                            return PlanView(
                                              continuePressed: continueAction,
                                            );
                                          },
                                          routes: [
                                            GoRoute(
                                                name: AppViews.masterpieceView,
                                                path: _Paths.masterpieceView,
                                                builder: (context, state) {
                                                  final Map? data =
                                                      state.extra as Map?;
                                                  final model = data?['model'];
                                                  return MasterpieceView(
                                                    model: model,
                                                  );
                                                },
                                                routes: [
                                                  GoRoute(
                                                      name: AppViews.photosView,
                                                      path: _Paths.photosView,
                                                      builder:
                                                          (context, state) {
                                                        final Map? data =
                                                            state.extra as Map?;
                                                        final List<MediaModel>
                                                            models =
                                                            data?['models'] ??
                                                                [];
                                                        final bool isProfile =
                                                            data?['isProfile'] ??
                                                                false;

                                                        final String? title =
                                                            data?['title'];

                                                        return PhotosView(
                                                          models: models,
                                                          isProfile: isProfile,
                                                          title: title,
                                                        );
                                                      })
                                                ])
                                          ])
                                    ])
                              ]),
                        ])
                  ]),
            ]),
      ]),
]);

abstract class _Paths {
  static const init = '/';
  static const signIn = AppViews.signIn;
  static const verify = AppViews.verify;
  static const forgot = AppViews.forgot;
  static const newPassword = AppViews.newPassword;

  // TODO
  // static const String homePageRoute = '/';
  static const String homePageRoute = '/${AppViews.homePageRoute}';
  static const String officePageRoute = AppViews.officePageRoute;
  static const String disclaimarPageRoute = AppViews.disclaimarPageRoute;
  static const String instructionPageRoute = AppViews.instructionPageRoute;
  static const String uploadingPhotosPageRoute =
      AppViews.uploadingPhotosPageRoute;

  // static const String generateView = AppViews.generateView;
  static const String resultView = AppViews.resultView;
  static const String settingsView = AppViews.settingsView;
  static const String legalView = AppViews.legalView;
  static const String documentView = AppViews.documentView;
  static const String faqView = AppViews.faqView;

  // static const String image = 'image';

  static const String allStyles = AppViews.allStyles;
  static const String imageWithBackground = AppViews.imageWithBackground;
  static const String genderView = AppViews.genderView;
  static const String planView = AppViews.planView;
  static const String masterpieceView = AppViews.masterpieceView;

  static const String toolsView = AppViews.toolsView;
  static const String backgroundsView = AppViews.backgroundsView;

  static const String enhanceView = AppViews.enhanceView;

  // static const String studyingView = AppViews.studyingView;
  static const String photosView = AppViews.photosView;
}
