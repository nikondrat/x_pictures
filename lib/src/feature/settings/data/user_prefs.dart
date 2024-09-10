import 'user_prefs_datasource.dart';

abstract interface class UserPrefsRepository {
  /// Get theme
  Future<bool?> getIsReceiveNewsletters();

  /// Set theme
  Future<void> setIsReceiveNewsletters(bool value);
}

/// Theme repository implementation
final class UserPrefsRepositoryImpl implements UserPrefsRepository {
  /// Create theme repository
  const UserPrefsRepositoryImpl({required UserPrefsDataSource source})
      : _source = source;

  final UserPrefsDataSource _source;

  @override
  Future<bool?> getIsReceiveNewsletters() => _source.getIsReceiveNewsletters();

  @override
  Future<void> setIsReceiveNewsletters(bool value) =>
      _source.setIsReceiveNewsletters(value);
}
