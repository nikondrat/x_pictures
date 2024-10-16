import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:intl/intl.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:x_pictures/src/core/components/rest_client/src/rest_client_dio.dart';
import 'package:x_pictures/src/data.dart';

final class InitializationProcessor {
  const InitializationProcessor(this.config);

  /// Application configuration
  final Config config;

  Future<Dependencies> _initDependencies() async {
    final sharedPreferences = await SharedPreferences.getInstance();
    const secureStorage = FlutterSecureStorage();
    final tokenStorage = TokenStorageImpl(storage: secureStorage);
    final restClient = await _initRestClient(secureStorage, tokenStorage);
    final errorTrackingManager = await _initErrorTrackingManager();
    final settingsStore = await _initSettingsStore(sharedPreferences);

    return Dependencies(
      restClient: restClient,
      tokenStorage: tokenStorage,
      secureStorage: secureStorage,
      sharedPreferences: sharedPreferences,
      settingsStore: settingsStore,
      errorTrackingManager: errorTrackingManager,
    );
  }

  Future<ErrorTrackingManager> _initErrorTrackingManager() async {
    final errorTrackingManager = SentryTrackingManager(
      logger,
      sentryDsn: config.sentryDsn,
      environment: config.environment.value,
    );

    if (config.enableSentry) {
      await errorTrackingManager.enableReporting();
    }

    return errorTrackingManager;
  }

  Future<SettingsStore> _initSettingsStore(SharedPreferences prefs) async {
    final localeRepository = LocaleRepositoryImpl(
      localeDataSource: LocaleDataSourceLocal(sharedPreferences: prefs),
    );

    final themeRepository = ThemeRepositoryImpl(
      themeDataSource: ThemeDataSourceLocal(
        sharedPreferences: prefs,
        codec: const ThemeModeCodec(),
      ),
    );
    final userPrefsRepository = UserPrefsRepositoryImpl(
        source: UserPrefsDataSourceLocal(sharedPreferences: prefs));

    final localeFuture = localeRepository.getLocale();
    final theme = await themeRepository.getTheme();
    final locale = await localeFuture;
    final isReceiveNewsletters =
        await userPrefsRepository.getIsReceiveNewsletters();

    final settingsStore = SettingsStore(
      localeRepository: localeRepository,
      themeRepository: themeRepository,
      userPrefsRepository: userPrefsRepository,
      receiveNewsletters: isReceiveNewsletters ?? true,
      locale: locale ?? Locale(Intl.systemLocale),
      appTheme: theme ??
          AppThemeStore(mode: ThemeMode.dark, seed: AppColors.kPrimaryColor),
    );
    return settingsStore;
  }

  // Initializes the REST client with the provided FlutterSecureStorage.
  Future<RestClient> _initRestClient(
      FlutterSecureStorage storage, TokenStorageImpl tokenStorage) async {
    final dio = Dio();
    final refreshClient = RefreshClientImpl(tokenStorage: tokenStorage);

    // Configure AuthInterceptor with tokenStorage and refreshClient
    final authInterceptor = AuthInterceptor(
      storage: tokenStorage,
      refreshClient: refreshClient,
      buildHeaders: (token) async {
        if (token != null) {
          return {'Authorization': 'Token $token'};
        }
        return {};
      },
    );

    // Add AuthInterceptor to Dio’s interceptors
    dio.interceptors.add(authInterceptor);
    dio.interceptors.add(LogInterceptor(
        requestBody: true,
        request: true,
        requestHeader: true,
        responseHeader: false,
        responseBody: true));

    return RestClientDio(baseUrl: config.apiUrl, dio: dio);
  }

  /// Initializes dependencies and returns the result of the initialization.
  ///
  /// This method may contain additional steps that need initialization
  /// before the application starts
  /// (for example, caching or enabling tracking manager)
  Future<InitializationResult> initialize() async {
    final stopwatch = Stopwatch()..start();

    logger.info('Initializing dependencies...');
    // initialize dependencies
    final dependencies = await _initDependencies();
    logger.info('Dependencies initialized');

    stopwatch.stop();
    final result = InitializationResult(
      dependencies: dependencies,
      msSpent: stopwatch.elapsedMilliseconds,
    );
    return result;
  }
}
