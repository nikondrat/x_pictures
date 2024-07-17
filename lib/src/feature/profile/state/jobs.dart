import 'dart:developer';

import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'jobs.g.dart';

class JobsStore extends _JobsStore with _$JobsStore {
  JobsStore({required super.restClient});
}

abstract class _JobsStore with Store {
  final RestClient restClient;

  _JobsStore({required this.restClient});

  JobsBody body = JobsBody(
    count: 0,
    total: 0,
    nextUrl: '',
    previousUrl: '',
    jobs: [],
  );

  @observable
  ObservableFuture<List<JobModel>> fetchJobsFuture = emptyResponse;

  @observable
  ObservableList<JobModel> jobs = ObservableList();

  @action
  Future<List<JobModel>> fetchJobs() async {
    final future = restClient.get(Endpoint().jobs).then((v) {
      body = JobsBody.fromJson(v!);

      return body.jobs;
    });
    fetchJobsFuture = ObservableFuture(future);

    return jobs = ObservableList.of(await future);
  }

  @computed
  bool get hasResults =>
      fetchJobsFuture != emptyResponse &&
      fetchJobsFuture.status == FutureStatus.fulfilled;

  static ObservableFuture<List<JobModel>> emptyResponse =
      ObservableFuture.value([]);
}
