import 'package:flex_color_scheme/flex_color_scheme.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'app_theme.g.dart';

class AppThemeStore extends _AppThemeStore with _$AppThemeStore {
  AppThemeStore({required super.mode, required super.seed});
}

abstract class _AppThemeStore with Store {
  _AppThemeStore({required this.mode, required this.seed})
      : lightTheme = FlexThemeData.light(
          useMaterial3: true,
          fontFamily: 'Rubik',
        ),
        darkTheme = FlexThemeData.dark(
            useMaterial3: true,
            fontFamily: 'Rubik',
            scaffoldBackground: AppColors.kBackgroundColor,
            surface: AppColors.kBackgroundColor,
            appBarBackground: AppColors.kBackgroundColor,
            surfaceTint: AppColors.kBackgroundColor,
            error: AppColors.kErrorColor,
            textTheme: const TextTheme(
                headlineMedium: TextStyle(
                    fontSize: 34,
                    fontFamily: 'Rubik',
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.5)),
            subThemesData: const FlexSubThemesData(
              appBarCenterTitle: true,
              appBarBackgroundSchemeColor: SchemeColor.background,
              filledButtonRadius: AppValues.kRadius,
              inputDecoratorFillColor: AppColors.kSecondaryColor,
              inputDecoratorRadius: AppValues.kRadius,
              inputDecoratorBorderType: FlexInputBorderType.outline,
              inputDecoratorUnfocusedBorderIsColored: false,
              chipRadius: AppValues.kRadius * 2,
            ),
            colors: const FlexSchemeColor(
                primary: AppColors.kPrimaryColor,
                secondary: AppColors.kSecondaryColor));

  /// The type of theme to use.
  @observable
  ThemeMode mode;

  /// The seed color to generate the [ColorScheme] from.
  @observable
  Color seed;

  /// The dark [ThemeData] for this [AppThemeStore].
  @observable
  ThemeData darkTheme;

  /// The light [ThemeData] for this [AppThemeStore].
  @observable
  ThemeData lightTheme;

  @action

  /// The [ThemeData] for this [AppThemeStore].
  /// This is computed based on the [mode].
  ThemeData computeTheme() {
    switch (mode) {
      case ThemeMode.light:
        return lightTheme;
      case ThemeMode.dark:
        return darkTheme;
      case ThemeMode.system:
        return PlatformDispatcher.instance.platformBrightness == Brightness.dark
            ? darkTheme
            : lightTheme;
    }
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is AppThemeStore && seed == other.seed && mode == other.mode;

  @override
  int get hashCode => Object.hash(seed, mode);
}
