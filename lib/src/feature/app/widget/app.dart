import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:reactive_forms/reactive_forms.dart';
import 'package:sentry_flutter/sentry_flutter.dart';
import 'package:x_pictures/src/data.dart';

/// [App] is an entry point to the application.
///
/// Scopes that don't depend on widgets returned by [MaterialApp]
/// ([Directionality], [MediaQuery], [Localizations]) should be placed here.
class App extends StatelessWidget {
  const App({required this.result, super.key});

  /// The initialization result from the [InitializationProcessor]
  /// which contains initialized dependencies.
  final InitializationResult result;

  @override
  Widget build(BuildContext context) => DefaultAssetBundle(
        bundle: SentryAssetBundle(),
        child: MultiProvider(
          providers: [
            Provider(create: (context) => result.dependencies),
            Provider(
                create: (context) => UserStore(
                    tokenStorage: context.read<Dependencies>().tokenStorage,
                    restClient: context.read<Dependencies>().restClient)),
            Provider(create: (context) => HomeStore()),
            Provider(
                create: (context) => MediaBodyStore(
                      homeStore: context.read<HomeStore>(),
                    )),
            Provider(
                create: (context) => PacksStore(
                      restClient: context.read<Dependencies>().restClient,
                    )),
            Provider(
                create: (context) => LoraStore(
                      restClient: context.read<Dependencies>().restClient,
                    )),
            Provider(
                create: (context) => MediaBodyStore(
                      homeStore: context.read<HomeStore>(),
                    )),
          ],
          child: ReactiveFormConfig(validationMessages: {
            ValidationMessage.required: (error) => t.auth.errors.empty,
            ValidationMessage.email: (error) => t.auth.errors.email,
            ValidationMessage.minLength: (error) => t.auth.errors.min_length,
            ValidationMessage.mustMatch: (error) => t.auth.errors.must_match
          }, child: TranslationProvider(child: const MaterialContext())),
        ),
      );
}
