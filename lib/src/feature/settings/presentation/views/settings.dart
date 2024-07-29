import 'dart:io';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:settings_ui/settings_ui.dart';
import 'package:x_pictures/src/data.dart';

class SettingsView extends StatelessWidget {
  const SettingsView({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    final UserStore userStore = Provider.of<UserStore>(context);

    final bool isAndroid = Platform.isAndroid;
    // final bool isAndroid = false;

    return Scaffold(
        appBar: AppBar(
          leading: const CustomBackButton(),
          title: Text(t.settings.title),
        ),
        body: SettingsList(
          darkTheme: SettingsThemeData(
            titleTextColor: AppColors.kOutlineColor,
            settingsListBackground: colorScheme.surface,
            settingsSectionBackground: isAndroid
                ? colorScheme.surface
                : AppColors.kSecondaryAdditionallyColor,
          ),
          // platform: DevicePlatform.iOS,
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
                    '***${userStore.email.split('@').last}',
                    // '***@yandex.ru',
                    style: textTheme.bodyLarge,
                  ),
                  trailing: const Icon(Icons.arrow_forward_ios),
                ),
                SettingsTile.navigation(
                  title: Text(
                    t.settings.exit,
                    style:
                        textTheme.bodyLarge!.copyWith(color: colorScheme.error),
                  ),
                  onPressed: (context) {
                    userStore.logout();
                  },
                  trailing: const SizedBox.shrink(),
                ),
                if (isAndroid) SettingsTile(title: const Divider())
              ],
            ),
            SettingsSection(
                title: Text(
                  t.settings.subscription.title,
                  style: textTheme.titleMedium!
                      .copyWith(color: AppColors.kOutlineColor),
                ),
                tiles: [
                  SettingsTile.navigation(
                    title: Text(
                      userStore.user.typeVerbose,
                      // t.settings.trial,
                      style: textTheme.bodyLarge,
                    ),
                    trailing: const SizedBox.shrink(),
                  ),
                  SettingsTile.navigation(
                    title: Text(
                      t.settings.subscription.manage,
                      style: textTheme.bodyLarge!
                          .copyWith(color: colorScheme.primary),
                    ),
                    trailing: const SizedBox.shrink(),
                  ),
                  if (isAndroid) SettingsTile(title: const Divider())
                ]),
            SettingsSection(
                title: Text(
                  t.settings.help_center.title,
                  style: textTheme.titleMedium!
                      .copyWith(color: AppColors.kOutlineColor),
                ),
                tiles: [
                  SettingsTile.navigation(
                    title: Text(
                      t.settings.help_center.faq,
                      style: textTheme.bodyLarge,
                    ),
                    onPressed: (context) => router.goNamed(AppViews.faqView),
                    trailing: const Icon(Icons.arrow_forward_ios),
                  ),
                  SettingsTile.navigation(
                    title: Text(
                      t.settings.help_center.report,
                      style: textTheme.bodyLarge,
                    ),
                    trailing: const Icon(Icons.arrow_forward_ios),
                  ),
                  if (isAndroid) SettingsTile(title: const Divider())
                ]),
            SettingsSection(
                title: Text(
                  t.settings.notifications.title,
                  style: textTheme.titleMedium!
                      .copyWith(color: AppColors.kOutlineColor),
                ),
                tiles: [
                  SettingsTile.switchTile(
                    onToggle: (value) {},
                    initialValue: true,
                    activeSwitchColor: Platform.isIOS || Platform.isMacOS
                        ? colorScheme.primary
                        : null,
                    title: Text(
                      t.settings.notifications.receiveNews,
                      style: textTheme.bodyLarge,
                    ),
                  ),
                ]),
            SettingsSection(
                title: Text(
                  t.settings.other.title,
                  style: textTheme.titleMedium!
                      .copyWith(color: AppColors.kOutlineColor),
                ),
                tiles: [
                  SettingsTile.navigation(
                    title: Text(
                      t.settings.other.sendFeedback,
                      style: textTheme.bodyLarge,
                    ),
                    trailing: const Icon(Icons.arrow_forward_ios),
                  ),
                  SettingsTile.navigation(
                    title: Text(
                      t.settings.other.legal.title,
                      style: textTheme.bodyLarge,
                    ),
                    onPressed: (context) => router.goNamed(AppViews.legalView),
                    trailing: const Icon(Icons.arrow_forward_ios),
                  ),
                  SettingsTile.navigation(
                    title: Text(
                      t.settings.other.rate_us,
                      style: textTheme.bodyLarge!
                          .copyWith(color: colorScheme.primary),
                    ),
                    trailing: const SizedBox.shrink(),
                  ),
                  if (isAndroid) SettingsTile(title: const Divider())
                ]),
            SettingsSection(
                title: Text(
                  t.settings.delete.title,
                  style: textTheme.titleMedium!
                      .copyWith(color: AppColors.kOutlineColor),
                ),
                tiles: [
                  SettingsTile.navigation(
                    title: Text(
                      t.settings.delete.account,
                      style: textTheme.bodyLarge!
                          .copyWith(color: colorScheme.error),
                    ),
                    onPressed: (context) {
                      userStore.deleteAccount();
                    },
                    trailing: const SizedBox.shrink(),
                  ),
                  const _TextSection(),
                ]),
          ],
        ));
  }
}

class _TextSection extends AbstractSettingsTile {
  const _TextSection();

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    return Padding(
      padding: const EdgeInsets.symmetric(
          horizontal: AppValues.kPadding, vertical: AppValues.kPadding / 2),
      child: Text(
        t.settings.delete.note,
        style: textTheme.labelLarge!.copyWith(color: AppColors.kOutlineColor),
      ),
    );
  }
}
