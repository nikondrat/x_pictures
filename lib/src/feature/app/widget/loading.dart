import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:loading_animation_widget/loading_animation_widget.dart';
import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

class LoadingWidget<T> extends StatelessWidget {
  final ObservableFuture<T> future;

  final Widget Function(T) builder;
  final Widget? loadingWidget;
  final Widget? errorWidget;
  final Widget? emptyData;

  const LoadingWidget({
    super.key,
    required this.future,
    required this.builder,
    this.loadingWidget,
    this.errorWidget,
    this.emptyData,
  });

  @override
  Widget build(BuildContext context) {
    return Observer(
      builder: (context) {
        switch (future.status) {
          case FutureStatus.pending:
            return loadingWidget ??
                Center(
                    child: LoadingAnimationWidget.fourRotatingDots(
                        color: AppColors.kPrimaryColor, size: 30));
          case FutureStatus.rejected:
            return errorWidget ??
                const Center(
                  child: Text('error loading'),
                );
          case FutureStatus.fulfilled:
            final T data = future.value as T;

            if (data == null || (data is List && data.isEmpty)) {
              return emptyData ?? const SizedBox.shrink();
            }

            return builder(data);
        }
      },
    );
  }
}
