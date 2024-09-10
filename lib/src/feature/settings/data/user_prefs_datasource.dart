import 'package:x_pictures/src/data.dart';

abstract interface class UserPrefsDataSource {
  /// Get theme
  Future<bool?> getIsReceiveNewsletters();

  /// Set theme
  Future<void> setIsReceiveNewsletters(bool value);
}

final class UserPrefsDataSourceLocal extends PreferencesDao
    implements UserPrefsDataSource {
  const UserPrefsDataSourceLocal({required super.sharedPreferences});

  PreferencesEntry<bool> get _isReceiveNewsletters =>
      boolEntry('settings.isReceiveNewsletters');

  @override
  Future<bool?> getIsReceiveNewsletters() async {
    final data = _isReceiveNewsletters.read();

    return data;
  }

  @override
  Future<void> setIsReceiveNewsletters(bool value) async {
    await _isReceiveNewsletters.set(value);
  }
}
