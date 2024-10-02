import 'dart:io';

import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:settings_ui/settings_ui.dart';
import 'package:x_pictures/src/data.dart';

class LegalView extends StatelessWidget {
  const LegalView({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;
    final bool isAndroid = Platform.isAndroid;

    return Scaffold(
        appBar: AppBar(
          leading: const CustomBackButton(),
          title: AutoSizeText(
            t.settings.other.legal.title,
            style: textTheme.bodyMedium!.copyWith(
              fontWeight: FontWeight.w700,
              fontSize: 17,
            ),
          ),
        ),
        body: SettingsList(
          darkTheme: SettingsThemeData(
            titleTextColor: AppColors.kOutlineColor,
            settingsListBackground: colorScheme.surface,
            settingsSectionBackground: isAndroid
                ? colorScheme.surface
                : AppColors.kSecondaryAdditionallyColor,
          ),
          platform: PlatformUtils.detectPlatform(context),
          sections: [
            SettingsSection(
              title: Text(
                t.settings.account.title,
                style: textTheme.titleMedium!
                    .copyWith(color: AppColors.kOutlineColor),
              ),
              tiles: <SettingsTile>[
                SettingsTile.navigation(
                  title: Text(
                    t.settings.other.legal.privacy_policy,
                    style: textTheme.bodyLarge,
                  ),
                  trailing: const Icon(Icons.arrow_forward_ios),
                  onPressed: (context) =>
                      router.goNamed(AppViews.documentView, extra: {
                    'title': t.settings.other.legal.privacy_policy,
                    'filePath': Assets.docs.privacyPolicy
                  }),
                ),
                SettingsTile.navigation(
                  title: Text(
                    t.settings.other.legal.terms_of_use,
                    style: textTheme.bodyLarge,
                  ),
                  trailing: const Icon(Icons.arrow_forward_ios),
                  onPressed: (context) => router.goNamed(AppViews.documentView,
                      extra: {
                        'title': t.settings.other.legal.terms_of_use,
                        'filePath': Assets.docs.terms
                      }),
                ),
              ],
            ),
          ],
        ));
  }
}
