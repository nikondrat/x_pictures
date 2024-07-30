import 'package:device_preview/device_preview.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

/// [MaterialContext] is an entry point to the material context.
///
/// This widget sets locales, themes and routing.
class MaterialContext extends StatelessWidget {
  const MaterialContext({super.key});

  // This global key is needed for [MaterialApp]
  // to work properly when Widgets Inspector is enabled.
  // static final _globalKey = GlobalKey();

  @override
  Widget build(BuildContext context) {
    final settings = Provider.of<Dependencies>(context).settingsStore;

    return ScreenUtilInit(
        designSize: const Size(375, 836),
        minTextAdapt: true,
        enableScaleText: () => false,
        splitScreenMode: true,
        builder: (context, child) {
          return Observer(builder: (_) {
            return MaterialApp.router(
              routerConfig: router,
              theme: settings.lightTheme,
              darkTheme: settings.darkTheme,
              themeMode: settings.themeMode,
              debugShowCheckedModeBanner: kDebugMode,
              localizationsDelegates: GlobalMaterialLocalizations.delegates,
              supportedLocales: AppLocaleUtils.supportedLocales,
              locale: TranslationProvider.of(context).flutterLocale,
              builder: DevicePreview.appBuilder,
            );
          });
        });
  }
}
