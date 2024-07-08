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
                              content: (state.extra as Map)['content'] ?? '',
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
                items: items,
              );
            }),
        GoRoute(
            path: _Paths.resultView,
            name: AppViews.resultView,
            builder: (context, state) {
              final Map? data = state.extra as Map?;
              final MediaModel? model = data?['model'];
              return GenerationResult(
                model: model,
              );
            }),
        GoRoute(
            name: AppViews.officePageRoute,
            path: _Paths.officePageRoute,
            builder: (context, state) {
              final Map? data = state.extra as Map?;
              final StyleModel model = data?['model'];
              return StyleView(
                model: model,
              );
            },
            routes: [
              GoRoute(
                name: AppViews.enhanceView,
                path: _Paths.enhanceView,
                builder: (context, state) {
                  final Map? data = state.extra as Map?;
                  final StyleModel model = data?['model'];
                  return EnhanceView(
                    model: model,
                  );
                },
              ),
              GoRoute(
                  name: AppViews.toolsView,
                  path: _Paths.toolsView,
                  builder: (context, state) {
                    final Map? data = state.extra as Map?;
                    final StyleModel model = data?['model'];
                    final bool isRemoveBackground =
                        data?['isRemoveBackground'] ?? false;
                    return ToolsView(
                      model: model,
                      isRemoveBackground: isRemoveBackground,
                    );
                  },
                  routes: [
                    GoRoute(
                        name: AppViews.backgroundsView,
                        path: _Paths.backgroundsView,
                        builder: (context, state) {
                          final Map? data = state.extra as Map?;
                          final StyleModel model = data?['model'];
                          return BackgroundsView(
                            model: model,
                          );
                        },
                        routes: [
                          GoRoute(
                              name: AppViews.imageWithBackground,
                              path: _Paths.imageWithBackground,
                              builder: (_, state) {
                                final Map map = state.extra as Map;
                                final StyleModel model =
                                    map['model'] as StyleModel;
                                return ImageWithBackgroundResultView(
                                    model: model);
                              })
                        ])
                  ]),
              GoRoute(
                  name: AppViews.disclaimarPageRoute,
                  path: _Paths.disclaimarPageRoute,
                  builder: (context, state) {
                    final Map? data = state.extra as Map?;
                    final StyleModel model = data?['model'];

                    return DisclaimarPage(
                      model: model,
                    );
                  },
                  routes: [
                    GoRoute(
                        name: AppViews.instructionPageRoute,
                        path: _Paths.instructionPageRoute,
                        builder: (context, state) {
                          final Map? data = state.extra as Map?;
                          final StyleModel model = data?['model'];
                          return InstructionPage(
                            model: model,
                          );
                        },
                        routes: [
                          GoRoute(
                              name: AppViews.uploadingPhotosPageRoute,
                              path: _Paths.uploadingPhotosPageRoute,
                              builder: (context, state) {
                                final Map? data = state.extra as Map?;
                                final StyleModel model = data?['model'];
                                return UploadingPhotosPage(
                                  model: model,
                                );
                              },
                              routes: [
                                GoRoute(
                                    name: AppViews.genderView,
                                    path: _Paths.genderView,
                                    builder: (context, state) {
                                      final Map? data = state.extra as Map?;
                                      final StyleModel model = data?['model'];
                                      return GenderView(
                                        model: model,
                                      );
                                    },
                                    routes: [
                                      GoRoute(
                                          name: AppViews.planView,
                                          path: _Paths.planView,
                                          builder: (context, state) {
                                            final Map? data =
                                                state.extra as Map?;
                                            final StyleModel model =
                                                data?['model'];
                                            return PlanView(
                                              model: model,
                                            );
                                          },
                                          routes: [
                                            GoRoute(
                                                name: AppViews.masterpieceView,
                                                path: _Paths.masterpieceView,
                                                builder: (context, state) {
                                                  final Map? data =
                                                      state.extra as Map?;
                                                  final StyleModel model =
                                                      data?['model'];
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
                                                        final List<String>
                                                            urls =
                                                            data?['urls'] ?? [];
                                                        // final StyleModel model =
                                                        //     data?['model'];
                                                        return PhotosView(
                                                          urls: urls,
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

  static const String studyingView = AppViews.studyingView;
  static const String photosView = AppViews.photosView;
}
