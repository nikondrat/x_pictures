class Endpoint {
  // Face2img
  static const String _face2img = 'face2img';

  /// Endpoint for packs
  String get packs => '$_face2img/packs';

  /// Endpoint for loras
  String get loras => '$_face2img/loras';

  /// Endpoint for jobs
  String get jobs => '$_face2img/jobs';

  /// White generate
  static const String _jobs = 'jobs';

  /// Endpoint for white generate
  String get whiteGenerate => '$_jobs/white-generate';

  /// Endpoint of filters for white generate
  String get filtersForGenerate => '$whiteGenerate/filters';

  // Profile
  static const _profiles = 'profiles';

  /// Endpoint for change password
  String get changePassword => '$_profiles/change-password';

  /// Endpoint for delete account
  String get deleteAccount => '$_profiles/delete-account';

  /// Endpoint for delete image
  String get deleteImage => '$_profiles/delete-image';

  /// Endpoint for get account info
  String get getAccountInfo => '$_profiles/me';

  /// Endpoint for update account
  String get updateAccount => '$_profiles/update';

  /// Endpoint for upload image
  String get uploadImage => '$_profiles/upload-image';

  /// Endpoint for add patreon
  String get patreon => '$_profiles/patreon';

  /// Endpoint for get patreon
  String get patreonInfo => '$patreon/info';

  // Users
  static const String _users = 'users';

  /// Base endpoint for password reset
  static const String _passwordReset = '$_users/password-reset';

  /// Base endpoint for social login
  static const String _socialLogin = '$_users/social-media';

  /// Endpoint for login
  String get login => '$_users/login';

  /// Endpoint for google auth
  String get googleAuth => '$_socialLogin/google-auth';

  /// Endpoint for register
  String get register => '$_users/register';

  /// Endpoint for send password reset
  String get sendReqPasswordReset => '$_passwordReset/send';

  /// Endpoint for set new password
  String get setNewPassword => '$_passwordReset/set';

  /// Endpoint for refresh verification
  String get refreshVerification => '$_users/refresh-verification';

  /// Endpoint for verification by token
  String get verificationByToken => '$_users/verification/';

  // Support

  static const String _support = 'support';

  /// Endpoint for send message to support
  String get sendSupportMessage => '$_support/create-message';

  // Shop
  static const String _shop = 'shop';

  // Callback
  static const String _callback = '$_shop/callback';

  /// Endpoint for emovegan
  String get emoveganCallback => '$_callback/emovegan';

  /// Endpoint for paypal
  String get paypalCallback => '$_callback/paypal-subscription';

  // Payment
  static const String _order = '$_shop/order';
  static const String _payment = '$_shop/payment';

  /// Endpoint for create order
  String get createOrder => '$_order/create-order';

  /// Endpoint for get payment orders
  String get paymentOrders => _payment;

  /// Endpoint for get payment gates
  String get paymentGates => '$_payment/gates';

  // Subscription
  static const String _subscription = '$_shop/subscription';

  /// Endpoint for cancel subscription
  String get cancelSubscription => '$_subscription/cancel';

  /// Endpoint for get all subscriptions
  String get getAllSubscriptions => '${_subscription}s';

  /// Endpoint for get shop tokens
  String get shopTokens => '$_shop/tokens';
}
