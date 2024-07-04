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

    return Scaffold(
        appBar: AppBar(
          title: Text(t.settings.other.legal.title),
        ),
        body: SettingsList(
          darkTheme: SettingsThemeData(
            titleTextColor: AppColors.kOutlineColor,
            settingsListBackground: colorScheme.surface,
            settingsSectionBackground: AppColors.kSecondaryAdditionallyColor,
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
                  onPressed: (context) => router.goNamed(AppViews.documentView,
                      extra: {
                        'title': t.settings.other.legal.privacy_policy,
                        'content': 'content'
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
                        'content': 'content'
                      }),
                ),
              ],
            ),
          ],
        ));
  }
}
