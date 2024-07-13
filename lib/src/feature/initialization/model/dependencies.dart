import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:x_pictures/src/data.dart';

/// Dependencies container
base class Dependencies {
  const Dependencies({
    required this.restClient,
    required this.tokenStorage,
    required this.secureStorage,
    required this.sharedPreferences,
    required this.settingsStore,
    required this.errorTrackingManager,
  });

  /// [RestClient] instance, used to send HTTP requests.
  final RestClient restClient;

  /// [TokenStorage] instance, used to store and retrieve Auth tokens.
  final TokenStorage tokenStorage;

  /// [FlutterSecureStorage] instance, used to securely store Key-Value pairs.
  final FlutterSecureStorage secureStorage;

  /// [SharedPreferences] instance, used to store Key-Value pairs.
  final SharedPreferences sharedPreferences;

  /// [SettingsStore] instance, used to manage theme and locale.
  final SettingsStore settingsStore;

  /// [ErrorTrackingManager] instance, used to report errors.
  final ErrorTrackingManager errorTrackingManager;
}

/// Result of initialization
final class InitializationResult {
  const InitializationResult({
    required this.dependencies,
    required this.msSpent,
  });

  /// The dependencies
  final Dependencies dependencies;

  /// The number of milliseconds spent
  final int msSpent;

  @override
  String toString() => '$InitializationResult('
      'dependencies: $dependencies, '
      'msSpent: $msSpent'
      ')';
}
